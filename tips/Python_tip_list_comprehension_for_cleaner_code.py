"""
Python Tip: List comprehension for cleaner code

Use list comprehensions instead of loops for creating lists. They are more concise, readable, and often faster.

Generated on: 2025-11-02
"""

# Traditional approach with loop
squares = []
for i in range(10):
    squares.append(i ** 2)

# Better approach with list comprehension
squares = [i ** 2 for i in range(10)]

# With conditional filtering
even_squares = [i ** 2 for i in range(10) if i % 2 == 0]
print(even_squares)  # [0, 4, 16, 36, 64]
