"""
Python Tip: Using enumerate for index and value

Instead of using range(len()), use enumerate() to get both index and value when iterating over a sequence. This is more Pythonic and readable.

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
