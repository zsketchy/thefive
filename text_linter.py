#!/usr/bin/env python3
"""
Text File Linter
Enforces rules:
- Maximum 5 lines per file
- Maximum 10 words per line
"""

import sys
import argparse
from pathlib import Path


class TextLinter:
    def __init__(self, max_lines=5, max_words_per_line=10):
        self.max_lines = max_lines
        self.max_words_per_line = max_words_per_line
        self.errors = []
    
    def lint_file(self, file_path):
        """Lint a text file and return errors if any."""
        self.errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            self.errors.append(f"Error: File '{file_path}' not found")
            return self.errors
        except Exception as e:
            self.errors.append(f"Error reading file '{file_path}': {e}")
            return self.errors
        
        # Check line count
        if len(lines) > self.max_lines:
            self.errors.append(
                f"Line count violation: File has {len(lines)} lines, "
                f"maximum allowed is {self.max_lines}"
            )
        
        # Check word count per line
        for line_num, line in enumerate(lines, 1):
            # Remove trailing newline for word count
            line_content = line.rstrip('\n\r')
            words = line_content.split()
            
            if len(words) > self.max_words_per_line:
                self.errors.append(
                    f"Word count violation on line {line_num}: "
                    f"Line has {len(words)} words, "
                    f"maximum allowed is {self.max_words_per_line}"
                )
        
        return self.errors
    
    def lint_directory(self, directory_path, file_pattern="*.txt"):
        """Lint all files matching pattern in directory."""
        directory = Path(directory_path)
        if not directory.exists():
            return [f"Directory '{directory_path}' not found"]
        
        all_errors = []
        for file_path in directory.glob(file_pattern):
            file_errors = self.lint_file(file_path)
            if file_errors:
                all_errors.append(f"\n=== {file_path} ===")
                all_errors.extend(file_errors)
        
        return all_errors


def main():
    parser = argparse.ArgumentParser(
        description="Lint text files for line and word count violations"
    )
    parser.add_argument(
        "files", 
        nargs="*", 
        help="Text files to lint (default: lint all .txt files in current directory)"
    )
    parser.add_argument(
        "--max-lines", 
        type=int, 
        default=5, 
        help="Maximum number of lines allowed (default: 5)"
    )
    parser.add_argument(
        "--max-words", 
        type=int, 
        default=10, 
        help="Maximum number of words per line (default: 10)"
    )
    parser.add_argument(
        "--directory", 
        help="Directory to lint (default: current directory)"
    )
    
    args = parser.parse_args()
    
    linter = TextLinter(args.max_lines, args.max_words)
    
    if args.files:
        # Lint specific files
        all_errors = []
        for file_path in args.files:
            errors = linter.lint_file(file_path)
            if errors:
                all_errors.append(f"\n=== {file_path} ===")
                all_errors.extend(errors)
        
        if all_errors:
            print("\n".join(all_errors))
            sys.exit(1)
        else:
            print("All files passed linting!")
    else:
        # Lint directory
        directory = args.directory or "."
        errors = linter.lint_directory(directory)
        
        if errors:
            print("\n".join(errors))
            sys.exit(1)
        else:
            print("All files passed linting!")


if __name__ == "__main__":
    main()
