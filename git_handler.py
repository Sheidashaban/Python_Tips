"""
Git Handler for Python Tip Agent
Manages Git operations: commit and push
"""

import os
from pathlib import Path
from git import Repo, GitCommandError
from typing import Optional


class GitHandler:
    """Handles Git operations for the tip repository"""
    
    def __init__(self, repo_path: str = ".", remote_url: Optional[str] = None):
        """
        Initialize Git handler
        
        Args:
            repo_path: Path to the Git repository
            remote_url: Remote repository URL (e.g., GitHub URL)
        """
        self.repo_path = Path(repo_path)
        self.remote_url = remote_url or os.getenv("GITHUB_REPO_URL")
        
        try:
            self.repo = Repo(self.repo_path)
        except Exception:
            # Initialize repo if it doesn't exist
            self.repo = Repo.init(self.repo_path)
            print(f"[OK] Initialized new Git repository at {self.repo_path}")
        
        # Set up remote if provided
        if self.remote_url:
            self._setup_remote()
    
    def _setup_remote(self):
        """Set up or update the remote origin"""
        try:
            if 'origin' in [remote.name for remote in self.repo.remotes]:
                origin = self.repo.remote('origin')
                if origin.url != self.remote_url:
                    origin.set_url(self.remote_url)
                    print(f"[OK] Updated remote origin to {self.remote_url}")
            else:
                self.repo.create_remote('origin', self.remote_url)
                print(f"[OK] Added remote origin: {self.remote_url}")
        except Exception as e:
            print(f"[WARNING] Could not set up remote: {e}")
    
    def commit_tip(self, tip_filepath: Path, tip_data: dict) -> bool:
        """
        Commit a new tip file to the repository
        
        Args:
            tip_filepath: Path to the tip file
            tip_data: Dictionary containing tip metadata
            
        Returns:
            True if commit successful, False otherwise
        """
        try:
            # Add the tip file
            self.repo.index.add([str(tip_filepath)])
            
            # Also add the history file if it exists
            history_file = self.repo_path / "tip_history.json"
            if history_file.exists():
                self.repo.index.add([str(history_file)])
            
            # Create commit message
            commit_message = f"Add Python Tip: {tip_data['headline']}\n\n"
            commit_message += f"Filename: {tip_data['filename']}\n"
            commit_message += f"Generated: {tip_data['date'][:10]}"
            
            # Commit
            self.repo.index.commit(commit_message)
            print(f"[OK] Committed: {tip_data['filename']}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error committing file: {e}")
            return False
    
    def push_to_remote(self, branch: str = "master") -> bool:
        """
        Push commits to the remote repository
        
        Args:
            branch: Branch name to push (default: master)
            
        Returns:
            True if push successful, False otherwise
        """
        try:
            if 'origin' not in [remote.name for remote in self.repo.remotes]:
                print("[ERROR] No remote 'origin' configured")
                return False
            
            origin = self.repo.remote('origin')
            
            # Try to push
            push_info = origin.push(branch)
            
            if push_info:
                print(f"[OK] Successfully pushed to {branch} branch")
                return True
            else:
                print("[WARNING] Push completed but no info returned")
                return True
                
        except GitCommandError as e:
            print(f"[ERROR] Error pushing to remote: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Unexpected error during push: {e}")
            return False
    
    def commit_and_push(self, tip_filepath: Path, tip_data: dict, branch: str = "master") -> bool:
        """
        Commit and push a tip in one operation
        
        Args:
            tip_filepath: Path to the tip file
            tip_data: Dictionary containing tip metadata
            branch: Branch name to push (default: master)
            
        Returns:
            True if both operations successful, False otherwise
        """
        if not self.commit_tip(tip_filepath, tip_data):
            return False
        
        return self.push_to_remote(branch)
    
    def get_status(self) -> str:
        """Get the current Git status"""
        try:
            return self.repo.git.status()
        except Exception as e:
            return f"Error getting status: {e}"
    
    def get_last_commit(self) -> Optional[str]:
        """Get the last commit message"""
        try:
            if self.repo.head.is_valid():
                return str(self.repo.head.commit.message)
            return None
        except Exception:
            return None


if __name__ == "__main__":
    # Test the Git handler
    from dotenv import load_dotenv
    load_dotenv()
    
    handler = GitHandler()
    print("\n=== Git Status ===")
    print(handler.get_status())
    
    last_commit = handler.get_last_commit()
    if last_commit:
        print("\n=== Last Commit ===")
        print(last_commit)

