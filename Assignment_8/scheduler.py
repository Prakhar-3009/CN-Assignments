# scheduler.py
"""
PART 3: Output Port Scheduling Simulation
-----------------------------------------
Implements:
1. Packet dataclass (contains IPs, payload, and priority)
2. FIFO (First Come First Served) scheduler
3. Priority scheduler
"""

from dataclasses import dataclass
from typing import List
import heapq


@dataclass
class Packet:
    source_ip: str
    dest_ip: str
    payload: str
    priority: int  # 0 = High, 1 = Medium, 2 = Low


def fifo_scheduler(packet_list: List[Packet]) -> List[Packet]:
    """
    FIFO (First-Come, First-Served) scheduling.
    Simply returns packets in the same arrival order.
    """
    return list(packet_list)


def priority_scheduler(packet_list: List[Packet]) -> List[Packet]:
    """
    Priority scheduling.
    Sends packets with higher priority (lower number) first.
    Stable order for same priority (preserves arrival order).
    """
    heap = []
    for idx, pkt in enumerate(packet_list):
        heapq.heappush(heap, (pkt.priority, idx, pkt))

    ordered = []
    while heap:
        _, _, pkt = heapq.heappop(heap)
        ordered.append(pkt)

    return ordered


# Optional self-test
if __name__ == "__main__":
    packets = [
        Packet("10.0.0.1", "10.0.0.2", "Data Packet 1", priority=2),
        Packet("10.0.0.3", "10.0.0.4", "Data Packet 2", priority=2),
        Packet("10.0.0.5", "10.0.0.6", "VOIP Packet 1", priority=0),
        Packet("10.0.0.7", "10.0.0.8", "Video Packet 1", priority=1),
        Packet("10.0.0.9", "10.0.0.10", "VOIP Packet 2", priority=0)
    ]
    fifo_result = fifo_scheduler(packets)
    priority_result = priority_scheduler(packets)
    print("FIFO:", [p.payload for p in fifo_result])
    print("Priority:", [p.payload for p in priority_result])
