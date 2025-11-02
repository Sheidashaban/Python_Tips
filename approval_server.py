"""
Flask Web Server for Tip Approval
Provides endpoints for approving/rejecting tips via email links
"""

from flask import Flask, render_template_string, request, redirect
import json
import secrets
from pathlib import Path
from datetime import datetime
from git_handler import GitHandler
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))

# Storage for pending approvals
PENDING_FILE = Path("pending_approvals.json")


def load_pending():
    """Load pending approvals from file"""
    if PENDING_FILE.exists():
        with open(PENDING_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_pending(data):
    """Save pending approvals to file"""
    with open(PENDING_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def add_pending_approval(tip_data: dict) -> str:
    """
    Add a tip to pending approvals
    Returns: approval token
    """
    token = secrets.token_urlsafe(32)
    pending = load_pending()
    pending[token] = {
        "tip_data": tip_data,
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }
    save_pending(pending)
    return token


SUCCESS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Tip {{ action }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 600px;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        .icon {
            font-size: 80px;
            margin-bottom: 20px;
        }
        .success { color: #28a745; }
        .rejected { color: #dc3545; }
        .error { color: #ffc107; }
        p {
            color: #666;
            font-size: 18px;
            line-height: 1.6;
        }
        .tip-info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }
        code {
            background: #e8e8e8;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: monospace;
        }
        a {
            color: #667eea;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon {{ status_class }}">{{ icon }}</div>
        <h1>{{ title }}</h1>
        <p>{{ message }}</p>
        {% if tip_name %}
        <div class="tip-info">
            <strong>Tip:</strong> {{ tip_name }}<br>
            <strong>Filename:</strong> <code>{{ filename }}</code>
        </div>
        {% endif %}
        {% if github_url %}
        <p>
            <a href="{{ github_url }}" target="_blank">View on GitHub →</a>
        </p>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    """Home page showing pending approvals"""
    pending = load_pending()
    pending_count = sum(1 for v in pending.values() if v['status'] == 'pending')
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Python Tip Approval System</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
                text-align: center;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .stat-card {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .stat-number {{
                font-size: 48px;
                font-weight: bold;
                color: #667eea;
            }}
            .stat-label {{
                color: #666;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🐍 Python Tip Approval System</h1>
            <p>Automated daily Python tips with email approval workflow</p>
        </div>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{pending_count}</div>
                <div class="stat-label">Pending Approvals</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(pending)}</div>
                <div class="stat-label">Total Requests</div>
            </div>
        </div>
        <p style="text-align: center; color: #666;">
            Check your email for approval links when new tips are generated.
        </p>
    </body>
    </html>
    """
    return html


@app.route('/approve/<token>')
def approve(token):
    """Approve a tip and push to GitHub"""
    pending = load_pending()
    
    if token not in pending:
        return render_template_string(
            SUCCESS_TEMPLATE,
            action="Error",
            status_class="error",
            icon="⚠️",
            title="Invalid or Expired Token",
            message="This approval link is invalid or has already been used.",
            tip_name=None,
            filename=None,
            github_url=None
        ), 404
    
    approval_data = pending[token]
    
    if approval_data['status'] != 'pending':
        return render_template_string(
            SUCCESS_TEMPLATE,
            action="Already Processed",
            status_class="error",
            icon="⚠️",
            title="Already Processed",
            message=f"This tip has already been {approval_data['status']}.",
            tip_name=approval_data['tip_data']['headline'],
            filename=approval_data['tip_data']['filename'],
            github_url=None
        )
    
    tip_data = approval_data['tip_data']
    
    try:
        # Initialize Git handler
        git_handler = GitHandler(
            repo_path=".",
            remote_url=os.getenv("GITHUB_REPO_URL", "https://github.com/Sheidashaban/Python_Tips")
        )
        
        # Get the tip file path
        tip_filepath = Path("tips") / tip_data['filename']
        
        if not tip_filepath.exists():
            raise Exception(f"Tip file not found: {tip_filepath}")
        
        # Commit and push
        branch = os.getenv("GITHUB_BRANCH", "master")
        success = git_handler.commit_and_push(tip_filepath, tip_data, branch)
        
        if success:
            # Update status
            approval_data['status'] = 'approved'
            approval_data['approved_at'] = datetime.now().isoformat()
            pending[token] = approval_data
            save_pending(pending)
            
            # Construct GitHub URL
            repo_url = os.getenv("GITHUB_REPO_URL", "https://github.com/Sheidashaban/Python_Tips")
            github_url = f"{repo_url}/blob/{branch}/tips/{tip_data['filename']}"
            
            return render_template_string(
                SUCCESS_TEMPLATE,
                action="Approved",
                status_class="success",
                icon="✅",
                title="Tip Approved & Pushed!",
                message="The Python tip has been successfully pushed to your GitHub repository.",
                tip_name=tip_data['headline'],
                filename=tip_data['filename'],
                github_url=github_url
            )
        else:
            raise Exception("Git push failed")
            
    except Exception as e:
        return render_template_string(
            SUCCESS_TEMPLATE,
            action="Error",
            status_class="error",
            icon="❌",
            title="Push Failed",
            message=f"There was an error pushing to GitHub: {str(e)}",
            tip_name=tip_data['headline'],
            filename=tip_data['filename'],
            github_url=None
        ), 500


@app.route('/reject/<token>')
def reject(token):
    """Reject a tip"""
    pending = load_pending()
    
    if token not in pending:
        return render_template_string(
            SUCCESS_TEMPLATE,
            action="Error",
            status_class="error",
            icon="⚠️",
            title="Invalid or Expired Token",
            message="This rejection link is invalid or has already been used.",
            tip_name=None,
            filename=None,
            github_url=None
        ), 404
    
    approval_data = pending[token]
    tip_data = approval_data['tip_data']
    
    # Update status
    approval_data['status'] = 'rejected'
    approval_data['rejected_at'] = datetime.now().isoformat()
    pending[token] = approval_data
    save_pending(pending)
    
    # Optionally delete the tip file
    tip_filepath = Path("tips") / tip_data['filename']
    if tip_filepath.exists():
        tip_filepath.unlink()
        print(f"🗑️ Deleted rejected tip: {tip_filepath}")
    
    return render_template_string(
        SUCCESS_TEMPLATE,
        action="Rejected",
        status_class="rejected",
        icon="❌",
        title="Tip Rejected",
        message="The Python tip has been rejected and will not be pushed to GitHub.",
        tip_name=tip_data['headline'],
        filename=tip_data['filename'],
        github_url=None
    )


@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "python-tip-approval-server"}, 200


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"\n{'='*60}")
    print(f"🚀 Python Tip Approval Server Starting")
    print(f"{'='*60}")
    print(f"📍 URL: http://localhost:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

