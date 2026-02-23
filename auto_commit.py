#!/usr/bin/env python3
"""
auto_commit.py
Automated GitHub activity generator.
Creates 1-3 commits with timestamp entries in a log file.
"""

import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_git_command(command: list[str]) -> bool:
    """
    Execute a git command and return success status.
    
    Args:
        command: List of command arguments (e.g., ['git', 'add', '.'])
    
    Returns:
        bool: True if command succeeded, False otherwise
    """
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ {' '.join(command)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running {' '.join(command)}")
        print(f"  stderr: {e.stderr}")
        return False


def create_log_entry(commit_number: int, total_commits: int) -> str:
    """
    Generate a formatted log entry with timestamp.
    
    Args:
        commit_number: Current commit number in the batch
        total_commits: Total commits planned for this run
    
    Returns:
        str: Formatted log entry string
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    day_name = now.strftime("%A")
    
    entry = f"[{timestamp}] Activity log - {day_name} - Commit {commit_number}/{total_commits}\n"
    return entry


def generate_commit_message(commit_number: int) -> str:
    """
    Generate a descriptive commit message.
    
    Args:
        commit_number: Current commit number in the batch
    
    Returns:
        str: Commit message string
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    
    messages = [
        f"Update activity log - {date_str} #{commit_number}",
        f"Daily log entry - {date_str} ({time_str})",
        f"Activity update #{commit_number} - {date_str}",
        f"Log update - {now.strftime('%B %d, %Y')} #{commit_number}",
        f"Automated activity entry - {date_str} #{commit_number}",
    ]
    
    return random.choice(messages)


def append_to_log(entry: str, log_file: Path) -> bool:
    """
    Append an entry to the activity log file.
    
    Args:
        entry: The log entry to append
        log_file: Path to the log file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create file with header if it doesn't exist
        if not log_file.exists():
            header = "# Activity Log\n\nAutomated activity entries:\n\n"
            log_file.write_text(header)
        
        # Append the new entry
        with open(log_file, "a") as f:
            f.write(entry)
        
        print(f"✓ Added entry to {log_file}")
        return True
    except IOError as e:
        print(f"✗ Error writing to log file: {e}")
        return False


def make_commit(commit_number: int, total_commits: int, log_file: Path) -> bool:
    """
    Create a single commit with a log entry.
    
    Args:
        commit_number: Current commit number
        total_commits: Total commits for this run
        log_file: Path to the log file
    
    Returns:
        bool: True if commit succeeded, False otherwise
    """
    # Create log entry
    entry = create_log_entry(commit_number, total_commits)
    if not append_to_log(entry, log_file):
        return False
    
    # Stage changes
    if not run_git_command(["git", "add", "."]):
        return False
    
    # Create commit
    message = generate_commit_message(commit_number)
    if not run_git_command(["git", "commit", "-m", message]):
        return False
    
    return True


def main():
    """Main function to orchestrate the automated commits."""
    print("=" * 50)
    print("GitHub Auto-Commit Script")
    print("=" * 50)
    print()
    
    # Configuration
    log_file = Path("activity_log.md")
    
    # Determine number of commits (1-3)
    num_commits = random.randint(1, 3)
    print(f"📊 Generating {num_commits} commit(s) for today...")
    print()
    
    # Track successful commits
    successful_commits = 0
    
    # Create commits
    for i in range(1, num_commits + 1):
        print(f"--- Commit {i}/{num_commits} ---")
        if make_commit(i, num_commits, log_file):
            successful_commits += 1
        print()
    
    # Summary
    print("=" * 50)
    print(f"✅ Completed: {successful_commits}/{num_commits} commits")
    print("=" * 50)
    
    # Return appropriate exit code
    if successful_commits == 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
