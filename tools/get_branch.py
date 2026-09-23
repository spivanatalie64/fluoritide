import sys
import re
from html.parser import HTMLParser

class BranchParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.branches = []
        self.in_branch_li = False

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            for attr, value in attrs:
                if attr == "class" and "branch" in value.split():
                    self.in_branch_li = True
        elif tag == "a" and self.in_branch_li:
            self.capture_text = True

    def handle_endtag(self, tag):
        if tag == "li":
            self.in_branch_li = False
        elif tag == "a" and self.in_branch_li:
            self.capture_text = False

    def handle_data(self, data):
        if self.in_branch_li and getattr(self, 'capture_text', False):
            self.branches.append(data.strip())

# Read HTML from stdin
html_content = sys.stdin.read()
parser = BranchParser()
parser.feed(html_content)
if parser.branches:
    print(parser.branches[-1])
