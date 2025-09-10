# Ai-Code-Humanizer
## Code Humanizer AI

A lightweight Python chatbot that takes raw code (Python, JavaScript, C++, etc.) and turns it into human-readable explanations with inline comments.
It also provides a quick complexity analysis to give you a sense of how "heavy" your code is.

---

## Features

- Language detection (Python, JavaScript, Java, C/C++, C#, PHP, SQL, …)
- Inline comments added above functions, classes, assignments, loops, etc.
- Complexity analysis (lines, functions, classes, loops, conditionals)
- Natural language explanation of the code structure
- Interactive chatbot mode (help, quit, paste code directly)

---

 ## Demo mode with a sample function

# Installation

Clone/download this repo and make the script executable:

git clone https://github.com/yourusername/code-humanizer-ai.git
cd code-humanizer-ai
chmod +x code_humanizer.py


You’ll need Python 3.7+.
No external dependencies are required — it only uses the standard library. ✅

---

## Usage

Chatbot Mode (default)
Run the chatbot and paste in your code:
python code_humanizer.py


# Example session:

Code Humanizer Chatbot (type 'help' or 'quit')
You: def add_numbers(a, b): return a + b
--- Humanized Code ---
# Define function: Add Numbers
def add_numbers(a, b): return a + b

--- Explanation ---
Language guessed: python
Lines of code: 1  |  Complexity: Low (6 pts)
- Has 1 function(s)

Demo Mode

Runs a built-in example function to show off how it works:

python code_humanizer.py demo


# Output:

Original:
 def calc_total(nums, tax):
     total = 0
     for n in nums:
         total += n
     return total + total * tax

With comments:
 # Define function: Calculate Total
 def calc_total(nums, tax):
     # Assign a value to a variable
     total = 0
     # Loop through stuff
     for n in nums:
         # Do some math and save it
         total += n
     # Give back the result
     return total + total * tax

# Explanation:
 Language guessed: python
 Lines of code: 4  |  Complexity: Low (19 pts)
 - Has 1 function(s)
 - Uses 1 loop(s)
 - Uses 1 conditional(s)

---

## Project Structure
code_humanizer.py   # Main script
README.md           # Documentation (this file)

---

## Notes

The language detection is regex-based → not 100% accurate.
Comments are intentionally friendly & simple, not compiler-level precise.
Works best with short functions, classes, and educational code.

---

## Future Ideas

Smarter language detection (AST parsing for Python, JS)
Deeper complexity metrics (cyclomatic complexity, nesting)
Web UI / Streamlit playground
Save/export humanized code
