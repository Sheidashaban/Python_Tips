"""
Python Tip: Dictionary get method with default value

Use the get() method to safely retrieve dictionary values with a default fallback, avoiding KeyError exceptions.

Generated on: 2025-11-02
"""

# Without get() - may raise KeyError
user = {'name': 'Alice', 'age': 30}
# email = user['email']  # This would raise KeyError

# With get() - returns None if key doesn't exist
email = user.get('email')
print(f"Email: {email}")  # Email: None

# With get() and custom default value
email = user.get('email', 'not provided')
print(f"Email: {email}")  # Email: not provided
