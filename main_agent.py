"""
Main Python Tip Agent
Orchestrates daily tip generation, email approval, and GitHub push
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from tip_generator import TipGenerator
from email_handler import EmailHandler
from git_handler import GitHandler
from approval_server import add_pending_approval

# Load environment variables
load_dotenv()


class PythonTipAgent:
    """Main agent that orchestrates the daily tip workflow"""
    
    def __init__(self):
        self.tip_generator = TipGenerator(tips_directory="tips")
        self.email_handler = EmailHandler()
        self.git_handler = GitHandler(
            repo_path=".",
            remote_url=os.getenv("GITHUB_REPO_URL")
        )
    
    def generate_and_send_daily_tip(self):
        """
        Main workflow:
        1. Generate a new tip
        2. Save it to file
        3. Create approval token
        4. Send email with approval link
        """
        print("\n" + "="*60)
        print("Python Tip Agent - Daily Run")
        print("="*60 + "\n")
        
        # Step 1: Generate tip
        print("[1/4] Generating new Python tip...")
        tip_data = self.tip_generator.generate_tip()
        
        if not tip_data:
            print("[WARNING] No new tips available (all predefined tips used)")
            print("[TIP] Consider adding OpenAI API key for unlimited tips")
            return False
        
        print(f"[OK] Generated: {tip_data['headline']}")
        print(f"[OK] Filename: {tip_data['filename']}")
        
        # Step 2: Save tip to file
        print("\n[2/4] Saving tip to file...")
        tip_filepath = self.tip_generator.save_tip(tip_data)
        print(f"[OK] Saved to: {tip_filepath}")
        
        # Step 3: Create pending approval
        print("\n[3/4] Creating approval token...")
        approval_token = add_pending_approval(tip_data)
        print(f"[OK] Token created: {approval_token[:16]}...")
        
        # Step 4: Send email
        print("\n[4/4] Sending approval email...")
        email_sent = self.email_handler.send_approval_email(tip_data, approval_token)
        
        if email_sent:
            print(f"[OK] Email sent to {self.email_handler.recipient_email}")
            print("\n" + "="*60)
            print("SUCCESS: Daily tip workflow completed!")
            print("ACTION REQUIRED: Check your email to approve or reject the tip")
            print("="*60 + "\n")
            return True
        else:
            print("[WARNING] Email not sent (credentials may not be configured)")
            print("[TIP] The tip is saved and can be manually committed")
            print("\nManual approval instructions:")
            print(f"   1. Review the tip at: {tip_filepath}")
            print(f"   2. To approve, run: python manual_approve.py {approval_token}")
            print(f"   3. To reject, delete the file")
            print("="*60 + "\n")
            return False
    
    def check_status(self):
        """Check the current status of the agent"""
        print("\n" + "="*60)
        print("Python Tip Agent Status")
        print("="*60 + "\n")
        
        # Check Git status
        print("Git Repository Status:")
        print(self.git_handler.get_status())
        print()
        
        # Check history
        history = self.tip_generator.history
        print(f"Total tips generated: {len(history['tips'])}")
        
        if history['tips']:
            print("\nRecent tips:")
            for tip in history['tips'][-5:]:
                print(f"  - {tip['headline']} ({tip['date'][:10]})")
        
        print("\n" + "="*60 + "\n")


def main():
    """Main entry point"""
    agent = PythonTipAgent()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "status":
            agent.check_status()
        elif command == "run":
            agent.generate_and_send_daily_tip()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python main_agent.py [run|status]")
    else:
        # Default: run the daily tip generation
        agent.generate_and_send_daily_tip()


if __name__ == "__main__":
    main()

