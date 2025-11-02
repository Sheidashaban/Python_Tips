"""
Scheduler for Python Tip Agent
Runs the agent daily at a specified time
"""

import schedule
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from main_agent import PythonTipAgent

load_dotenv()


def run_daily_tip():
    """Execute the daily tip generation"""
    print(f"\n⏰ Scheduled run triggered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    agent = PythonTipAgent()
    agent.generate_and_send_daily_tip()


def start_scheduler():
    """Start the scheduler"""
    # Get schedule time from environment or use default (9:00 AM)
    schedule_time = os.getenv("DAILY_RUN_TIME", "09:00")
    
    print("="*60)
    print("🕐 Python Tip Agent Scheduler")
    print("="*60)
    print(f"📅 Scheduled to run daily at: {schedule_time}")
    print(f"🚀 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print("\n⏳ Waiting for scheduled time...")
    print("   (Press Ctrl+C to stop)\n")
    
    # Schedule the daily job
    schedule.every().day.at(schedule_time).do(run_daily_tip)
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n⛔ Scheduler stopped by user")
        print("="*60)


if __name__ == "__main__":
    start_scheduler()

