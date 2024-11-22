import blessed
from datetime import datetime
from typing import NoReturn
from ui_components import UIComponent
from system_stats import SystemMonitor

class WinTop:
    def __init__(self):
        self.term = blessed.Terminal()
        self.ui = UIComponent(self.term)
        self.monitor = SystemMonitor()

    def render(self) -> None:
        stats = self.monitor.get_system_stats()
        
        output = []
        output.append(self.term.home + self.term.clear)
        output.append(f"{self.term.bold('WinTop')} - {datetime.now().strftime('%H:%M:%S')}")
        output.append(self.term.blue("=" * self.term.width))
        
        # CPU section (2 columns) with System Resources on the right
        output.append(self.ui.create_header("CPU Usage and System Resources"))
        
        # Prepare system resources info
        mem_bar = self.ui.create_bar(stats.memory.percent)
        swap_bar = self.ui.create_bar(stats.swap.percent)
        resources_lines = [
            f"Memory: {self.ui.format_bytes(stats.memory.used)}/{self.ui.format_bytes(stats.memory.total)} {mem_bar}",
            f"Swap: {self.ui.format_bytes(stats.swap.used)}/{self.ui.format_bytes(stats.swap.total)} {swap_bar}"
        ]
        
        # CPU layout in two columns with resources on right
        cpu_count = len(stats.cpu_percent)
        mid_point = cpu_count // 2
        for i in range(mid_point):
            left_bar = self.ui.create_bar(stats.cpu_percent[i])
            right_bar = self.ui.create_bar(stats.cpu_percent[i + mid_point])
            resources_line = resources_lines[i] if i < len(resources_lines) else ""
            output.append(
                f"{self.term.bold(f'CPU{i:2d}')} {stats.cpu_percent[i]:5.1f}% {left_bar}    "
                f"{self.term.bold(f'CPU{i+mid_point:2d}')} {stats.cpu_percent[i+mid_point]:5.1f}% {right_bar}    "
                f"{resources_line}"
            )
        
        # Process section with fancy table
        output.append(self.ui.create_header("Top Processes"))
        
        # Table borders
        TOP_LEFT = '┌'
        TOP_RIGHT = '┐'
        BOTTOM_LEFT = '└'
        BOTTOM_RIGHT = '┘'
        HORIZONTAL = '─'
        VERTICAL = '│'
        T_DOWN = '┬'
        T_UP = '┴'
        T_CROSS = '┼'
        
        # Column widths - adjusted for better alignment
        pid_w, name_w, cpu_w, mem_w = 15, 35, 15, 15
        
        # Table header with perfect alignment
        header_line = f"{TOP_LEFT}{HORIZONTAL * pid_w}{T_DOWN}{HORIZONTAL * name_w}{T_DOWN}{HORIZONTAL * cpu_w}{T_DOWN}{HORIZONTAL * mem_w}{TOP_RIGHT}"
        title_line = f"{VERTICAL}{self.term.bold('PID'):^{pid_w}}{VERTICAL}{self.term.bold('Name'):^{name_w}}{VERTICAL}{self.term.bold('CPU%'):^{cpu_w}}{VERTICAL}{self.term.bold('MEM%'):^{mem_w}}{VERTICAL}"
        separator = f"├{'─' * pid_w}┼{'─' * name_w}┼{'─' * cpu_w}┼{'─' * mem_w}┤"
        
        output.append(header_line)
        output.append(title_line)
        output.append(separator)
        
        # Process rows with truncated names
        for pid, name, cpu, mem in stats.processes[:10]:
            # Truncate long process names and add ellipsis
            truncated_name = name[:name_w-3] + '...' if len(name) > name_w else name.ljust(name_w)
            output.append(f"{VERTICAL}{pid:^{pid_w}}{VERTICAL}{truncated_name:<{name_w}}{VERTICAL}{cpu:^{cpu_w}.1f}{VERTICAL}{mem:^{mem_w}.1f}{VERTICAL}")
        
        # Table bottom
        bottom_line = f"{BOTTOM_LEFT}{HORIZONTAL * pid_w}{T_UP}{HORIZONTAL * name_w}{T_UP}{HORIZONTAL * cpu_w}{T_UP}{HORIZONTAL * mem_w}{BOTTOM_RIGHT}"
        output.append(bottom_line)
        
        output.append(self.term.blue("\nPress 'q' to quit"))
        print('\n'.join(output))

    def run(self) -> NoReturn:
        with self.term.fullscreen(), self.term.hidden_cursor(), self.term.cbreak():
            while True:
                self.render()
                if self.term.inkey(timeout=0.5) == 'q':  # Reduced from 2 to 0.5 seconds for faster updates
                    break

def main():
    WinTop().run()

if __name__ == "__main__":
    main()
