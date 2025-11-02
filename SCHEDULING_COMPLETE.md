# ✅ Daily Tips Scheduled at 10:00 AM

## 🎉 Your Schedule is Set!

The Python Tip Agent is now configured to send daily tips at **10:00 AM**.

---

## 🚀 How to Start

### Option 1: Simple Start (Keep Window Open)

**Double-click:** `start_scheduler_10am.bat`

Or in terminal:
```bash
python scheduler.py
```

**What you'll see:**
```
============================================================
🕐 Python Tip Agent Scheduler
============================================================
📅 Scheduled to run daily at: 10:00
🚀 Started at: 2025-11-02 19:45:00
============================================================

⏳ Waiting for scheduled time...
   (Press Ctrl+C to stop)
```

**Keep this window open** and you'll receive an email every day at 10 AM! 📧

---

### Option 2: Windows Task Scheduler (Automatic)

For automatic running even after restart:

**Right-click:** `setup_windows_task.bat` → **Run as Administrator**

This will:
- ✅ Create a Windows scheduled task
- ✅ Run automatically at 10 AM daily
- ✅ Continue even after computer restart
- ✅ No need to keep terminal open

**To verify it worked:**
1. Press `Win + R`
2. Type `taskschd.msc` and press Enter
3. Look for "Python Tip Agent Daily" in the task list

---

## 📅 What Happens Daily at 10:00 AM

1. **🤖 Agent generates** a new Python tip (`.ipynb` format)
2. **📧 Email sent** to Sheida.shaban18@gmail.com
3. **✉️ You receive** beautiful HTML email with:
   - Tip explanation
   - Code example
   - **Green "Approve" button**
   - **Red "Reject" button**
4. **✅ You click "Approve"**
5. **🚀 Tip automatically pushed** to GitHub
6. **🎉 Your repository grows!**

---

## 🔍 Check Current Settings

Your configuration in `.env`:
```env
DAILY_RUN_TIME=10:00
RECIPIENT_EMAIL=Sheida.shaban18@gmail.com
GITHUB_REPO_URL=https://ghp_...@github.com/Sheidashaban/Python_Tips.git
```

---

## 🧪 Test It Now (Optional)

Don't want to wait until 10 AM? Test immediately:

```bash
python main_agent.py run
```

This will:
- Generate a tip right now
- Send you an email immediately
- You can test the approve workflow

---

## 📊 Monitor the Scheduler

When running `python scheduler.py`, you'll see:

**Before 10 AM:**
```
⏳ Waiting for scheduled time...
```

**At 10:00 AM exactly:**
```
⏰ Scheduled run triggered at 2025-11-03 10:00:00

============================================================
Python Tip Agent - Daily Run
============================================================

[1/4] Generating new Python tip...
[OK] Generated: Context managers with statement
[OK] Filename: Python_tip_context_managers_with_statement.ipynb

[2/4] Saving tip to file...
[OK] Saved to: tips\Python_tip_context_managers_with_statement.ipynb

[3/4] Creating approval token...
[OK] Token created: xyz123...

[4/4] Sending approval email...
[OK] Email sent to Sheida.shaban18@gmail.com

SUCCESS: Daily tip workflow completed!
============================================================
```

---

## ⏰ Change the Time (Optional)

Want a different time? Edit `.env`:

```env
# Examples:
DAILY_RUN_TIME=08:30  # 8:30 AM
DAILY_RUN_TIME=14:00  # 2:00 PM
DAILY_RUN_TIME=20:00  # 8:00 PM
```

Then restart the scheduler.

---

## 🛑 Stop the Scheduler

**If using `python scheduler.py`:**
- Press `Ctrl+C` in the terminal window

**If using Windows Task Scheduler:**
1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Find "Python Tip Agent Daily"
3. Right-click → **Disable** (temporarily) or **Delete** (permanently)

---

## ✅ Summary

- ✅ **Schedule set**: 10:00 AM daily
- ✅ **File format**: `.ipynb` (Jupyter Notebooks)
- ✅ **Email**: Sheida.shaban18@gmail.com
- ✅ **GitHub**: Auto-push on approval
- ✅ **Ready to go!**

---

## 📞 Troubleshooting

### Scheduler doesn't send email
- Check SENDER_EMAIL and SENDER_PASSWORD in `.env`
- Verify Gmail App Password is correct
- Run `python main_agent.py run` to test manually

### No new tips available
- Add `OPENAI_API_KEY` to `.env` for unlimited tips
- I've added 3 new tips (f-strings, context managers, *args/**kwargs)

### Windows Task doesn't run
- Right-click `setup_windows_task.bat` → Run as Administrator
- Check Task Scheduler for errors
- Make sure Python is in system PATH

### Approval links don't work
- Make sure approval server is running: `python approval_server.py`
- Or use manual approval: `python manual_approve.py <token>`

---

## 🎁 Bonus Tips

**Check if task is scheduled:**
```powershell
schtasks /query /tn "Python Tip Agent Daily"
```

**View scheduler logs (real-time):**
```bash
python scheduler.py
```

**Generate tip immediately:**
```bash
python main_agent.py run
```

---

## 🎉 You're All Set!

Your Python Tip Agent will now automatically:
- 📧 Email you at 10:00 AM daily
- 📚 Build your Python knowledge
- 🚀 Grow your GitHub repository
- 🎓 Share Python best practices

**Enjoy your automated learning journey!** 🐍✨

---

**First email arrives:** Tomorrow at 10:00 AM
**Repository:** https://github.com/Sheidashaban/Python_Tips

