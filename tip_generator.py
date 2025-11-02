"""
Python Tip Generator Agent
Generates daily Python tips with code snippets using OpenAI API
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
import openai


class TipGenerator:
    """Generates Python tips and manages tip files"""
    
    def __init__(self, tips_directory: str = "tips", history_file: str = "tip_history.json"):
        self.tips_directory = Path(tips_directory)
        self.tips_directory.mkdir(exist_ok=True)
        self.history_file = Path(history_file)
        self.history = self._load_history()
        
        # Initialize OpenAI API
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
    
    def _load_history(self) -> Dict:
        """Load history of generated tips"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return {"tips": []}
    
    def _save_history(self):
        """Save history of generated tips"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def _slugify(self, text: str) -> str:
        """Convert text to a slug format"""
        # Convert to lowercase and replace spaces with underscores
        text = text.lower().strip()
        # Remove special characters
        text = re.sub(r'[^\w\s-]', '', text)
        # Replace spaces and multiple underscores with single underscore
        text = re.sub(r'[-\s]+', '_', text)
        return text
    
    def _is_duplicate(self, shortname: str) -> bool:
        """Check if a tip with this shortname already exists"""
        # Check in history
        for tip in self.history["tips"]:
            if tip.get("shortname") == shortname:
                return True
        
        # Check if file exists
        filename = f"Python_tip_{shortname}.ipynb"
        return (self.tips_directory / filename).exists()
    
    def generate_tip(self) -> Optional[Dict[str, str]]:
        """
        Generate a new Python tip using OpenAI API
        Returns: Dict with 'headline', 'shortname', 'content', 'filename'
        """
        if not self.api_key:
            # Fallback to predefined tips if no API key
            return self._generate_fallback_tip()
        
        try:
            prompt = """Generate a unique and useful Python programming tip that includes:
1. A clear, concise headline (max 10 words)
2. A brief explanation (2-3 sentences)
3. A practical code example demonstrating the tip
4. Comments explaining the code

Format your response as:
HEADLINE: [headline]
EXPLANATION: [explanation]
CODE:
[code here]

Focus on practical, intermediate-level Python tips that developers find valuable."""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Python expert who creates helpful programming tips."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            return self._parse_api_response(content)
            
        except Exception as e:
            print(f"Error generating tip with API: {e}")
            return self._generate_fallback_tip()
    
    def _parse_api_response(self, content: str) -> Dict[str, str]:
        """Parse the API response into structured format"""
        lines = content.split('\n')
        headline = ""
        explanation = ""
        code_lines = []
        current_section = None
        
        for line in lines:
            if line.startswith("HEADLINE:"):
                headline = line.replace("HEADLINE:", "").strip()
                current_section = "headline"
            elif line.startswith("EXPLANATION:"):
                explanation = line.replace("EXPLANATION:", "").strip()
                current_section = "explanation"
            elif line.startswith("CODE:"):
                current_section = "code"
            elif current_section == "code":
                code_lines.append(line)
            elif current_section == "explanation" and line.strip():
                explanation += " " + line.strip()
        
        code = "\n".join(code_lines).strip()
        
        # Generate shortname and check for duplicates
        shortname = self._slugify(headline)
        counter = 1
        original_shortname = shortname
        while self._is_duplicate(shortname):
            shortname = f"{original_shortname}_{counter}"
            counter += 1
        
        filename = f"Python_tip_{shortname}.ipynb"
        
        # Create Jupyter notebook content
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        f"# Python Tip: {headline}\n",
                        "\n",
                        f"{explanation}\n",
                        "\n",
                        f"**Generated on:** {datetime.now().strftime('%Y-%m-%d')}"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": code.split('\n')
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "name": "python",
                    "version": "3.12.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        full_content = json.dumps(notebook_content, indent=2)
        
        return {
            "headline": headline,
            "shortname": shortname,
            "content": full_content,
            "filename": filename,
            "date": datetime.now().isoformat(),
            "code": code,
            "explanation": explanation
        }
    
    def _generate_fallback_tip(self) -> Dict[str, str]:
        """Generate a fallback tip when API is not available"""
        tips = [
            {
                "headline": "Using enumerate for index and value",
                "explanation": "Instead of using range(len()), use enumerate() to get both index and value when iterating over a sequence. This is more Pythonic and readable.",
                "code": '''# Bad approach
items = ['apple', 'banana', 'cherry']
for i in range(len(items)):
    print(f"{i}: {items[i]}")

# Better approach with enumerate
items = ['apple', 'banana', 'cherry']
for index, item in enumerate(items):
    print(f"{index}: {item}")

# Start counting from 1 instead of 0
for index, item in enumerate(items, start=1):
    print(f"{index}: {item}")'''
            },
            {
                "headline": "Dictionary get method with default value",
                "explanation": "Use the get() method to safely retrieve dictionary values with a default fallback, avoiding KeyError exceptions.",
                "code": '''# Without get() - may raise KeyError
user = {'name': 'Alice', 'age': 30}
# email = user['email']  # This would raise KeyError

# With get() - returns None if key doesn't exist
email = user.get('email')
print(f"Email: {email}")  # Email: None

# With get() and custom default value
email = user.get('email', 'not provided')
print(f"Email: {email}")  # Email: not provided'''
            },
            {
                "headline": "List comprehension for cleaner code",
                "explanation": "Use list comprehensions instead of loops for creating lists. They are more concise, readable, and often faster.",
                "code": '''# Traditional approach with loop
squares = []
for i in range(10):
    squares.append(i ** 2)

# Better approach with list comprehension
squares = [i ** 2 for i in range(10)]

# With conditional filtering
even_squares = [i ** 2 for i in range(10) if i % 2 == 0]
print(even_squares)  # [0, 4, 16, 36, 64]'''
            },
            {
                "headline": "Using f-strings for formatting",
                "explanation": "F-strings (formatted string literals) provide a concise and readable way to embed expressions inside string literals. They're faster and more readable than older formatting methods.",
                "code": '''name = "Alice"
age = 30
city = "Paris"

# Old way with %
message = "My name is %s, I'm %d years old, from %s" % (name, age, city)

# Better with .format()
message = "My name is {}, I'm {} years old, from {}".format(name, age, city)

# Best with f-strings (Python 3.6+)
message = f"My name is {name}, I'm {age} years old, from {city}"
print(message)

# F-strings can include expressions
print(f"Next year I'll be {age + 1} years old")'''
            },
            {
                "headline": "Context managers with statement",
                "explanation": "Use context managers (with statement) to ensure resources are properly managed and cleaned up, even if exceptions occur. Most commonly used with file operations.",
                "code": '''# Without context manager (bad practice)
file = open('example.txt', 'r')
data = file.read()
file.close()  # What if an error occurs before this?

# With context manager (recommended)
with open('example.txt', 'r') as file:
    data = file.read()
    # File automatically closes when leaving the block

# Multiple context managers
with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
    for line in infile:
        outfile.write(line.upper())'''
            },
            {
                "headline": "Using *args and **kwargs",
                "explanation": "*args allows a function to accept any number of positional arguments, while **kwargs allows any number of keyword arguments. These make functions more flexible.",
                "code": '''# *args for variable positional arguments
def sum_all(*args):
    return sum(args)

print(sum_all(1, 2, 3))  # 6
print(sum_all(1, 2, 3, 4, 5))  # 15

# **kwargs for variable keyword arguments
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="Paris")

# Combining regular args with *args and **kwargs
def flexible_function(required, *args, default="yes", **kwargs):
    print(f"Required: {required}")
    print(f"Args: {args}")
    print(f"Default: {default}")
    print(f"Kwargs: {kwargs}")

flexible_function("must have", 1, 2, 3, default="no", extra="data")'''
            }
        ]
        
        # Select a tip that hasn't been used yet
        for tip_template in tips:
            shortname = self._slugify(tip_template["headline"])
            if not self._is_duplicate(shortname):
                filename = f"Python_tip_{shortname}.ipynb"
                
                # Create Jupyter notebook content
                notebook_content = {
                    "cells": [
                        {
                            "cell_type": "markdown",
                            "metadata": {},
                            "source": [
                                f"# Python Tip: {tip_template['headline']}\n",
                                "\n",
                                f"{tip_template['explanation']}\n",
                                "\n",
                                f"**Generated on:** {datetime.now().strftime('%Y-%m-%d')}"
                            ]
                        },
                        {
                            "cell_type": "code",
                            "execution_count": None,
                            "metadata": {},
                            "outputs": [],
                            "source": tip_template["code"].split('\n')
                        }
                    ],
                    "metadata": {
                        "kernelspec": {
                            "display_name": "Python 3",
                            "language": "python",
                            "name": "python3"
                        },
                        "language_info": {
                            "name": "python",
                            "version": "3.12.0"
                        }
                    },
                    "nbformat": 4,
                    "nbformat_minor": 4
                }
                
                full_content = json.dumps(notebook_content, indent=2)
                
                return {
                    "headline": tip_template["headline"],
                    "shortname": shortname,
                    "content": full_content,
                    "filename": filename,
                    "date": datetime.now().isoformat(),
                    "code": tip_template["code"],
                    "explanation": tip_template["explanation"]
                }
        
        return None
    
    def save_tip(self, tip_data: Dict[str, str]) -> Path:
        """Save the tip to a file and update history"""
        filepath = self.tips_directory / tip_data["filename"]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(tip_data["content"])
        
        # Update history
        self.history["tips"].append({
            "headline": tip_data["headline"],
            "shortname": tip_data["shortname"],
            "filename": tip_data["filename"],
            "date": tip_data["date"]
        })
        self._save_history()
        
        return filepath


if __name__ == "__main__":
    # Test the tip generator
    generator = TipGenerator()
    tip = generator.generate_tip()
    
    if tip:
        print(f"Generated tip: {tip['headline']}")
        print(f"Filename: {tip['filename']}")
        filepath = generator.save_tip(tip)
        print(f"Saved to: {filepath}")
    else:
        print("No new tips available")


