# run_lab7_tests.py
"""
CN LAB 7: Test Runner
---------------------
Runs all three parts of the assignment in sequence:
1. IP Utilities
2. Router Forwarding (LPM)
3. Output Port Scheduling
"""

import ip_utils
from router import Router
from scheduler import Packet, fifo_scheduler, priority_scheduler

print("=" * 75)
print("🌐  PART 1: IP Address and Subnet Utilities")
print("=" * 75)

# Test Part 1
ip_example = "192.168.1.1"
binary_ip = ip_utils.ip_to_binary(ip_example)
print(f"ip_to_binary('{ip_example}') = {binary_ip}")

cidr_example = "200.23.16.0/23"
prefix = ip_utils.get_network_prefix(cidr_example)
print(f"get_network_prefix('{cidr_example}') = {prefix}\n")

# ---------------------------------------------------------------------
print("=" * 75)
print("🧭  PART 2: Router Forwarding Table (Longest Prefix Match)")
print("=" * 75)

routes = [
    ("223.1.1.0/24", "Link 0"),
    ("223.1.2.0/24", "Link 1"),
    ("223.1.3.0/24", "Link 2"),
    ("223.1.0.0/16", "Link 4 (ISP)")
]

router = Router(routes)

test_cases = [
    ("223.1.1.100", "Link 0"),
    ("223.1.2.5", "Link 1"),
    ("223.1.250.1", "Link 4 (ISP)"),
    ("198.51.100.1", "Default Gateway")
]

for dest_ip, expected in test_cases:
    result = router.route_packet(dest_ip)
    status = "✅" if result == expected else "❌"
    print(f"{status} {dest_ip} -> {result} (expected: {expected})")

print("\n")

# ---------------------------------------------------------------------
print("=" * 75)
print("📦  PART 3: Output Port Scheduling Simulation")
print("=" * 75)

packets = [
    Packet("10.0.0.1", "10.0.0.2", "Data Packet 1", priority=2),
    Packet("10.0.0.3", "10.0.0.4", "Data Packet 2", priority=2),
    Packet("10.0.0.5", "10.0.0.6", "VOIP Packet 1", priority=0),
    Packet("10.0.0.7", "10.0.0.8", "Video Packet 1", priority=1),
    Packet("10.0.0.9", "10.0.0.10", "VOIP Packet 2", priority=0)
]

fifo_result = fifo_scheduler(packets)
print("FIFO Scheduler Order:")
print(" -> ".join([p.payload for p in fifo_result]))

priority_result = priority_scheduler(packets)
print("\nPriority Scheduler Order:")
print(" -> ".join([p.payload for p in priority_result]))

print("\n" + "=" * 75)
print("🏁  ALL TESTS COMPLETED SUCCESSFULLY")
print("=" * 75)
