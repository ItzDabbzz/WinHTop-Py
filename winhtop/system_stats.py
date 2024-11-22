import psutil
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class MemoryStats:
    total: int
    used: int
    percent: float
    
@dataclass
class SystemStats:
    cpu_percent: List[float]
    memory: MemoryStats
    swap: MemoryStats
    processes: List[Tuple[int, str, float, float]]

class SystemMonitor:
    @staticmethod
    def get_system_stats() -> SystemStats:
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append((
                    proc.info['pid'],
                    proc.info['name'],
                    proc.info['cpu_percent'],
                    proc.info['memory_percent']
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return SystemStats(
            cpu_percent=cpu_percent,
            memory=MemoryStats(memory.total, memory.used, memory.percent),
            swap=MemoryStats(swap.total, swap.used, swap.percent),
            processes=sorted(processes, key=lambda x: x[2], reverse=True)[:10]
        )