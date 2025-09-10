#!/usr/bin/env python3
"""
Code Humanizer AI 

This script is basically a chatbot that takes in code (Python, JS, C++, etc.)
and spits out explanations, adds friendly comments, and tries to make sense
of it all in plain English. 
"""

import re
import time  # I don’t think I actually use this anywhere, but leaving it here anyway
from datetime import datetime
from typing import Dict, Optional


class CodeHumanizer:
    """Handles the main logic for adding comments + explaining code"""

    def __init__(self):
        # Some quick and dirty regex signatures for language guessing
        self.language_patterns = {
            'python': [r'def\s+\w+\s*\(', r'import\s+\w+', r'print\s*\(', r'if\s+__name__'],
            'javascript': [r'function\s+\w+\s*\(', r'console\.log', r'const\s+\w+', r'=>'],
            'java': [r'public\s+class', r'System\.out', r'public\s+static\s+void'],
            'cpp': [r'#include\s*<', r'std::', r'cout\s*<<', r'int\s+main'],
            'c': [r'#include\s*<.*\.h>', r'printf\s*\(', r'int\s+main'],
            'csharp': [r'using\s+System', r'Console\.WriteLine', r'public\s+class'],
            'php': [r'<\?php', r'\$\w+', r'echo\s+'],
            'sql': [r'SELECT\s+', r'FROM\s+', r'WHERE\s+'],
        }

    def detect_language(self, code_snippet: str) -> str:
        """Tries to guess what language the code is in (not 100% foolproof)."""
        lang_scores = {}
        for lang, patterns in self.language_patterns.items():
            hits = sum(len(re.findall(pat, code_snippet, re.IGNORECASE)) for pat in patterns)
            lang_scores[lang] = hits

        # Pick whichever had the most hits, unless none matched
        return max(lang_scores, key=lang_scores.get) if max(lang_scores.values()) > 0 else 'unknown'

    def get_comment_prefix(self, lang: str) -> str:
        """Figure out what comment symbol we should use (#, //, --, etc.)."""
        common_prefix = {
            'python': '#',
            'javascript': '//',
            'java': '//',
            'cpp': '//',
            'c': '//',
            'csharp': '//',
            'php': '//',
            'sql': '--',
            'unknown': '#'
        }
        return common_prefix.get(lang, '#')

    def make_function_name_readable(self, func_name: str) -> str:
        """
        Converts camelCase/snake_case into something readable.
        Example: calcTotal -> "Calc Total"
        """
        # Basic attempt at spacing camelCase
        nice_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', func_name)
        nice_name = nice_name.replace('_', ' ')

        # Try to be smart with common prefixes
        keywords = {
            'get': 'Get',
            'set': 'Set',
            'calc': 'Calculate',  # I added calc just because I use it a lot
            'create': 'Create',
            'delete': 'Delete',
            'update': 'Update',
            'process': 'Process',
            'parse': 'Parse'
        }

        for k, v in keywords.items():
            if func_name.lower().startswith(k):
                return f"{v} {nice_name[len(k):].strip()}".strip()

        return nice_name.title()

    def generate_line_comment(self, line: str, lang: str) -> Optional[str]:
        """
        Generates a one-liner comment for code lines.
        Not perfect, but good enough for most simple code.
        """
        line_txt = line.strip()

        # --- functions ---
        func_match = re.search(r'\b(def|function|func)\s+(\w+)', line_txt, re.IGNORECASE)
        if func_match:
            f_name = func_match.group(2)
            return f"Define function: {self.make_function_name_readable(f_name)}"

        # --- classes ---
        cls_match = re.search(r'\bclass\s+(\w+)', line_txt, re.IGNORECASE)
        if cls_match:
            return f"Define a new class named {cls_match.group(1)}"

        # --- assignments (super naive check) ---
        if '=' in line_txt and '==' not in line_txt:
            if 'input(' in line_txt:
                return "Take input from the user"
            elif any(op in line_txt for op in ['+', '-', '*', '/', '%']):
                return "Do some math and save it"
            else:
                return "Assign a value to a variable"

        # --- loops & conditions ---
        if 'for ' in line_txt and ' in ' in line_txt:
            return "Loop through stuff"
        if line_txt.startswith('while'):
            return "Repeat while condition holds true"
        if line_txt.startswith('if'):
            return "Check condition"
        if line_txt.startswith('elif') or 'else if' in line_txt:
            return "Alternative condition"
        if line_txt.startswith('else'):
            return "Fallback if nothing else matched"

        # --- misc ---
        if line_txt.startswith('return'):
            return "Give back the result"
        if 'print' in line_txt or 'console.log' in line_txt:
            return "Show something on screen"
        if 'import ' in line_txt or '#include' in line_txt:
            return "Bring in external library/module"

        return None

    def add_comments(self, code: str, lang: str) -> str:
        """Adds inline comments above lines of code."""
        out_lines = []
        prefix = self.get_comment_prefix(lang)

        for line in code.split('\n'):
            stripped = line.strip()
            if not stripped:
                out_lines.append(line)
                continue

            # Ignore if it's already a comment
            if stripped.startswith(prefix):
                out_lines.append(line)
                continue

            cmt = self.generate_line_comment(line, lang)
            if cmt:
                out_lines.append(f"{prefix} {cmt}")
            out_lines.append(line)

        return "\n".join(out_lines)

    def analyze_code(self, code: str) -> Dict[str, int]:
        """Super basic complexity analysis (don’t take it too seriously)."""
        lines = [l.strip() for l in code.splitlines() if l.strip()]

        stats = {
            'lines': len(lines),
            'functions': len(re.findall(r'\b(def|function)\s+\w+', code, re.IGNORECASE)),
            'classes': len(re.findall(r'\bclass\s+\w+', code, re.IGNORECASE)),
            'loops': len(re.findall(r'\b(for|while)\b', code, re.IGNORECASE)),
            'ifs': len(re.findall(r'\bif\b', code, re.IGNORECASE))
        }

        score = stats['lines'] + stats['functions'] * 5 + stats['classes'] * 10
        stats['complexity'] = score
        stats['level'] = 'Low' if score < 20 else 'Medium' if score < 50 else 'High'
        return stats

    def explain_code(self, code: str, lang: str, stats: Dict[str, int]) -> str:
        """Turns raw stats into a friendlier explanation."""
        out = []
        out.append(f"Language guessed: {lang}")
        out.append(f"Lines of code: {stats['lines']}  |  Complexity: {stats['level']} ({stats['complexity']} pts)")
        if stats['functions']:
            out.append(f"- Has {stats['functions']} function(s)")
        if stats['classes']:
            out.append(f"- Contains {stats['classes']} class(es)")
        if stats['loops']:
            out.append(f"- Uses {stats['loops']} loop(s)")
        if stats['ifs']:
            out.append(f"- Uses {stats['ifs']} conditional(s)")
        return "\n".join(out)

    def humanize_code(self, code: str) -> Dict[str, str]:
        """Main entry point: comment + explain."""
        lang = self.detect_language(code)
        commented = self.add_comments(code, lang)
        stats = self.analyze_code(code)
        explanation = self.explain_code(code, lang, stats)
        return {
            'original': code,
            'humanized': commented,
            'language': lang,
            'explanation': explanation,
            'metrics': stats
        }


class CodeHumanizerChatbot:
    """A very lightweight interactive chatbot wrapper."""

    def __init__(self):
        self.humanizer = CodeHumanizer()
        self.history = []  # I’m not really doing much with history, but storing it anyway

    def process(self, user_text: str) -> str:
        txt = user_text.strip()

        if txt.lower() in ['quit', 'exit']:
            return "👋 Exiting. Catch you later!"
        if txt.lower() == 'help':
            return "Paste some code and I'll add comments/explanation.\nCommands: help, quit"

        if 'def ' in txt or 'class ' in txt or 'function ' in txt:
            code = txt
            result = self.humanizer.humanize_code(code)
            return f"--- Humanized Code ---\n{result['humanized']}\n\n--- Explanation ---\n{result['explanation']}"
        else:
            return "Hmm, didn’t look like code to me. Try pasting a function or class."


def main():
    """CLI entry point (with a quick demo)."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        h = CodeHumanizer()
        example = """def calc_total(nums, tax):
    total = 0
    for n in nums:
        total += n
    return total + total * tax
"""
        print("Original:\n", example)
        result = h.humanize_code(example)
        print("\nWith comments:\n", result['humanized'])
        print("\nExplanation:\n", result['explanation'])
    else:
        bot = CodeHumanizerChatbot()
        print("🤖 Code Humanizer Chatbot (type 'help' or 'quit')")
        while True:
            try:
                user = input("You: ")
                resp = bot.process(user)
                print(resp)
                if "Exiting" in resp:
                    break
            except KeyboardInterrupt:
                print("\n👋 Goodbye (keyboard interrupt).")
                break


if __name__ == "__main__":
    main()
