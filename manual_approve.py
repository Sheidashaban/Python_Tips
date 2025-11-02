"""
Manual Approval Script
For approving tips without clicking email link
"""

import sys
import json
from pathlib import Path
from git_handler import GitHandler
from dotenv import load_dotenv
import os

load_dotenv()


def manual_approve(token: str):
    """Manually approve a tip using its token"""
    
    pending_file = Path("pending_approvals.json")
    
    if not pending_file.exists():
        print("[ERROR] No pending approvals found")
        return False
    
    with open(pending_file, 'r') as f:
        pending = json.load(f)
    
    if token not in pending:
        print(f"[ERROR] Token not found: {token}")
        print("\nAvailable tokens:")
        for t, data in pending.items():
            if data['status'] == 'pending':
                print(f"  - {t[:16]}... : {data['tip_data']['headline']}")
        return False
    
    approval_data = pending[token]
    tip_data = approval_data['tip_data']
    
    if approval_data['status'] != 'pending':
        print(f"[WARNING] This tip has already been {approval_data['status']}")
        return False
    
    print(f"\nApproving tip: {tip_data['headline']}")
    print(f"Filename: {tip_data['filename']}")
    
    try:
        # Initialize Git handler
        git_handler = GitHandler(
            repo_path=".",
            remote_url=os.getenv("GITHUB_REPO_URL", "https://github.com/Sheidashaban/Python_Tips")
        )
        
        # Get the tip file path
        tip_filepath = Path("tips") / tip_data['filename']
        
        if not tip_filepath.exists():
            print(f"[ERROR] Tip file not found: {tip_filepath}")
            return False
        
        # Commit and push
        branch = os.getenv("GITHUB_BRANCH", "master")
        print(f"\nCommitting and pushing to {branch}...")
        success = git_handler.commit_and_push(tip_filepath, tip_data, branch)
        
        if success:
            # Update status
            from datetime import datetime
            approval_data['status'] = 'approved'
            approval_data['approved_at'] = datetime.now().isoformat()
            pending[token] = approval_data
            
            with open(pending_file, 'w') as f:
                json.dump(pending, f, indent=2)
            
            print("[OK] Tip approved and pushed to GitHub!")
            return True
        else:
            print("[ERROR] Failed to push to GitHub")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manual_approve.py <approval_token>")
        sys.exit(1)
    
    token = sys.argv[1]
    success = manual_approve(token)
    sys.exit(0 if success else 1)

