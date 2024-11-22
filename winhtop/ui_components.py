import blessed
from typing import List, Tuple

class UIComponent:
    def __init__(self, term: blessed.Terminal):
        self.term = term
        
    def create_bar(self, percentage: float, width: int = 20) -> str:
        filled = int(width * percentage / 100)
        bar = f"[{'#' * filled}{'-' * (width - filled)}]"
        if percentage < 60:
            return self.term.green(bar)
        elif percentage < 80:
            return self.term.yellow(bar)
        return self.term.red(bar)

    def create_header(self, title: str) -> str:
        return f"\n{self.term.bold(title)}\n{self.term.blue('-' * self.term.width)}"

    def format_bytes(self, bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024:
                return f"{bytes:.2f}{unit}"
            bytes /= 1024
        return f"{bytes:.2f}TB"