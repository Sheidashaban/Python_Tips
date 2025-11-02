# 🚀 Quick Setup Guide

Follow these steps to get your Python Tip Agent up and running!

## ✅ Step 1: Configure Email Settings

To receive email notifications, you need to set up email credentials.

### For Gmail Users (Recommended):

1. **Enable 2-Factor Authentication** on your Google Account
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character password

3. **Create `.env` file**
   ```bash
   # Copy the template
   cp config.template .env
   ```

4. **Edit `.env` file** with your credentials:
   ```env
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_16_character_app_password
   RECIPIENT_EMAIL=Sheida.shaban18@gmail.com
   ```

## ✅ Step 2: Configure GitHub

### Option A: Using Personal Access Token (Easiest)

1. **Create a Personal Access Token**
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Give it a name: "Python Tips Agent"
   - Select scope: `repo` (full control of private repositories)
   - Click "Generate token"
   - **Copy the token** (you won't see it again!)

2. **Set up Git credentials**
   ```bash
   # When pushing, use your token as the password
   # Username: your_github_username
   # Password: your_personal_access_token
   ```

### Option B: Using SSH Keys

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@gmail.com"

# Copy the public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key

# Update remote URL in .env
GITHUB_REPO_URL=git@github.com:Sheidashaban/Python_Tips.git
```

## ✅ Step 3: Initialize Git Repository

```bash
# Initialize the repository
git init

# Add remote
git remote add origin https://github.com/Sheidashaban/Python_Tips

# Configure your identity
git config user.name "Sheida Shaban"
git config user.email "Sheida.shaban18@gmail.com"

# Create and push initial commit (optional)
git add .
git commit -m "Initial commit: Python Tip Agent setup"
git push -u origin master
```

**Note:** If your repository uses `main` instead of `master`, update `.env`:
```env
GITHUB_BRANCH=main
```

## ✅ Step 4: Test the System

### Test 1: Generate a Tip

```bash
python main_agent.py run
```

This will:
- Generate a new Python tip
- Save it to `tips/` folder
- Send you an email (if configured)
- Create an approval token

### Test 2: Start the Approval Server

```bash
python approval_server.py
```

Open your browser to http://localhost:5000 to see the dashboard.

### Test 3: Approve Manually (if email not configured)

```bash
# Use the token from Step 1 output
python manual_approve.py <your_token_here>
```

This will commit and push the tip to GitHub!

## ✅ Step 5: Set Up Daily Automation

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Python Tip Agent"
4. Trigger: Daily at 9:00 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `C:\Users\Sheida\Music\my_cursor_apps\Github_tips\main_agent.py run`
   - Start in: `C:\Users\Sheida\Music\my_cursor_apps\Github_tips`

### Using the Built-in Scheduler

```bash
# Runs forever, executing daily at configured time
python scheduler.py
```

**Note:** Keep this running in the background or as a service.

## 📧 Email Workflow

Once configured, here's what happens:

1. **9:00 AM Daily** (or your configured time)
   - Agent generates a new Python tip

2. **You receive an email** with:
   - The Python tip with code example
   - **Approve** button → Commits and pushes to GitHub
   - **Reject** button → Deletes the tip

3. **Click Approve**
   - Tip is automatically committed
   - Pushed to your GitHub repository
   - You see a confirmation page with link to GitHub

## 🔧 Configuration Options

Edit `.env` file to customize:

```env
# Change daily run time
DAILY_RUN_TIME=14:30  # 2:30 PM

# Change Flask port
FLASK_PORT=8080

# Add OpenAI for unlimited tips
OPENAI_API_KEY=sk-your-key-here

# Different email provider
SMTP_SERVER=smtp.office365.com  # For Outlook
SMTP_PORT=587
```

## 🎨 Optional: Add OpenAI API (Unlimited Tips)

Without OpenAI, you get 3 predefined tips. To generate unlimited unique tips:

1. **Get API Key**
   - Go to https://platform.openai.com/api-keys
   - Create new secret key

2. **Add to `.env`**
   ```env
   OPENAI_API_KEY=sk-your-key-here
   ```

3. **Test it**
   ```bash
   python main_agent.py run
   ```

## 🐛 Troubleshooting

### Email Not Sending?

- Check Gmail App Password (not your regular password)
- Verify 2FA is enabled
- Check SMTP settings match your provider

### Git Push Fails?

```bash
# Test Git credentials manually
git push origin master

# If it asks for credentials, enter:
# Username: your_github_username
# Password: your_personal_access_token
```

### Port Already in Use?

```env
# Change port in .env
FLASK_PORT=8080
```

Then access at http://localhost:8080

## ✨ You're All Set!

Your Python Tip Agent is now ready to:
- Generate daily Python tips automatically
- Email them to you for approval
- Push approved tips to GitHub
- Build your public Python tips repository

## 📞 Need Help?

Check the full README.md for more details or troubleshooting tips!

