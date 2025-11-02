# 🐍 Python Tip Agent

An automated Python agent that generates daily Python programming tips with code examples, sends them via email for approval, and pushes approved tips to your GitHub repository.

## ✨ Features

- **🤖 Automated Tip Generation**: Generates daily Python tips with practical code examples
- **📧 Email Approval Workflow**: Sends tips via email with approve/reject buttons
- **🔄 GitHub Integration**: Automatically commits and pushes approved tips to your repository
- **🌐 Web Interface**: Flask-based approval server with beautiful UI
- **🔐 Secure Token System**: Each tip gets a unique approval token
- **📊 Duplicate Detection**: Prevents generating the same tip twice
- **⏰ Scheduled Execution**: Runs daily at a configured time
- **🎨 Beautiful Email Templates**: HTML emails with syntax-highlighted code

## 📋 Requirements

- Python 3.8+
- Git configured with GitHub credentials
- Email account (Gmail recommended)
- OpenAI API key (optional, for unlimited tips)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Github_tips.git
cd Github_tips

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file from the template:

```bash
# Copy the configuration template
cp config.template .env
```

Edit `.env` with your credentials:

```env
# Email Configuration (Required)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=Sheida.shaban18@gmail.com

# GitHub Configuration
GITHUB_REPO_URL=https://github.com/Sheidashaban/Python_Tips
GITHUB_BRANCH=master

# OpenAI API (Optional - for unlimited tips)
OPENAI_API_KEY=sk-...

# Flask Server
APPROVAL_BASE_URL=http://localhost:5000

# Schedule
DAILY_RUN_TIME=09:00
```

#### 🔑 Getting Gmail App Password

1. Go to your [Google Account](https://myaccount.google.com/)
2. Select **Security**
3. Under "How you sign in to Google," select **2-Step Verification**
4. At the bottom, select **App passwords**
5. Generate a password for "Mail" and "Windows Computer"
6. Use this 16-character password in your `.env` file

### 3. GitHub Setup

Initialize the Git repository and set up the remote:

```bash
# Initialize git if not already done
git init

# Set up remote
git remote add origin https://github.com/Sheidashaban/Python_Tips

# Configure Git credentials
git config user.name "Your Name"
git config user.email "your_email@gmail.com"
```

For authentication, you have two options:

**Option A: Personal Access Token (Recommended)**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` scope
3. Use it as your password when pushing

**Option B: SSH Keys**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@gmail.com"

# Add to GitHub: Settings → SSH and GPG keys
cat ~/.ssh/id_ed25519.pub

# Use SSH URL
git remote set-url origin git@github.com:Sheidashaban/Python_Tips.git
```

## 📖 Usage

### Run Once (Manual)

Generate and send a tip immediately:

```bash
python main_agent.py run
```

### Start the Approval Server

The approval server must be running to handle email link clicks:

```bash
python approval_server.py
```

This starts a Flask server at `http://localhost:5000`

### Run the Scheduler

For automated daily execution:

```bash
python scheduler.py
```

This will run the agent every day at the configured time (default: 9:00 AM).

### Check Status

View the agent's current status:

```bash
python main_agent.py status
```

### Manual Approval

If you can't click the email link, approve manually:

```bash
python manual_approve.py <approval_token>
```

## 🔄 Complete Workflow

1. **Scheduled Trigger**: At 9:00 AM daily (or configured time)
2. **Tip Generation**: Agent generates a new Python tip
3. **File Creation**: Saves as `Python_tip_<shortname>.py` in `tips/` directory
4. **Email Sent**: Beautiful HTML email with tip and approve/reject buttons
5. **User Action**: You receive the email and click "Approve" or "Reject"
6. **GitHub Push**: If approved, the tip is automatically committed and pushed
7. **Confirmation**: You receive a confirmation page with a link to the tip on GitHub

## 📁 Project Structure

```
Github_tips/
├── main_agent.py              # Main orchestration script
├── tip_generator.py           # Tip generation logic
├── email_handler.py           # Email notification system
├── git_handler.py             # Git operations
├── approval_server.py         # Flask approval web server
├── scheduler.py               # Daily scheduler
├── manual_approve.py          # Manual approval tool
├── requirements.txt           # Python dependencies
├── config.template            # Configuration template
├── .gitignore                # Git ignore rules
├── README.md                  # This file
├── tips/                      # Generated tip files
│   └── Python_tip_*.py
├── tip_history.json          # Tip generation history
└── pending_approvals.json    # Pending approval tokens
```

## 🔧 Advanced Configuration

### Custom Tip Generation

Edit `tip_generator.py` to add custom fallback tips or modify the OpenAI prompt.

### Email Template Customization

Modify the HTML template in `email_handler.py` to customize the email appearance.

### Different Schedule Times

Change `DAILY_RUN_TIME` in `.env`:
```env
DAILY_RUN_TIME=14:30  # Run at 2:30 PM
```

### Multiple Recipients

Modify `email_handler.py` to send to multiple email addresses.

## 🐛 Troubleshooting

### Email Not Sending

- Verify Gmail App Password is correct
- Check 2-Factor Authentication is enabled
- Ensure "Less secure app access" is enabled (if not using App Password)
- Check SMTP settings match your email provider

### Git Push Fails

- Verify GitHub credentials are correct
- Check repository URL in `.env`
- Ensure you have push permissions to the repository
- Verify branch name (some repos use `main` instead of `master`)

### Approval Links Don't Work

- Ensure `approval_server.py` is running
- Check `APPROVAL_BASE_URL` in `.env` matches your server
- Verify port 5000 is not blocked by firewall

### "Module not found" Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 📊 Monitoring

View generated tips history:

```bash
cat tip_history.json
```

View pending approvals:

```bash
cat pending_approvals.json
```

Check Git status:

```bash
git status
git log --oneline
```

## 🔒 Security Notes

- Never commit your `.env` file
- Use App Passwords, not your main email password
- Keep your OpenAI API key secure
- Use HTTPS for production approval servers
- Consider using environment variables instead of `.env` in production

## 📝 Example Tip Output

```python
"""
Python Tip: Using enumerate for index and value

Instead of using range(len()), use enumerate() to get both index 
and value when iterating over a sequence. This is more Pythonic 
and readable.

Generated on: 2025-11-02
"""

# Bad approach
items = ['apple', 'banana', 'cherry']
for i in range(len(items)):
    print(f"{i}: {items[i]}")

# Better approach with enumerate
items = ['apple', 'banana', 'cherry']
for index, item in enumerate(items):
    print(f"{index}: {item}")

# Start counting from 1 instead of 0
for index, item in enumerate(items, start=1):
    print(f"{index}: {item}")
```

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📜 License

MIT License - feel free to use this project for your own learning and development.

## 🙏 Acknowledgments

- OpenAI for tip generation capabilities
- Flask for the web framework
- GitPython for Git operations
- Schedule for task scheduling

---

**Made with ❤️ for Python developers**

For questions or issues, please open an issue on GitHub.

