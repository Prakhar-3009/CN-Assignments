# router.py
"""
PART 2: Router Forwarding Table (Longest Prefix Match)
-------------------------------------------------------
Implements a Router class that performs:
- Longest Prefix Matching (LPM) using a forwarding table.
"""

from typing import List, Tuple
from ip_utils import ip_to_binary, get_network_prefix


class Router:
    def __init__(self, routes: List[Tuple[str, str]]):
        """
        Initialize router with a list of (CIDR, output_link) tuples.
        Example:
            [("223.1.1.0/24", "Link 0"), ("223.1.2.0/24", "Link 1")]
        """
        self._forwarding_table = []
        self._build_forwarding_table(routes)

    def _build_forwarding_table(self, routes: List[Tuple[str, str]]):
        """
        Build internal forwarding table with binary prefixes.
        Sort by prefix length (descending) for easy LPM.
        """
        table = []
        for cidr, out_link in routes:
            ip_part, prefix_len_str = cidr.split("/")
            prefix_len = int(prefix_len_str)
            prefix_bits = get_network_prefix(cidr)
            table.append((prefix_bits, prefix_len, out_link))

        # Sort longest prefix first
        table.sort(key=lambda x: x[1], reverse=True)
        self._forwarding_table = table

    def route_packet(self, dest_ip: str) -> str:
        """
        Perform Longest Prefix Match (LPM) and return output link.
        If no match, return "Default Gateway".
        """
        dest_bin = ip_to_binary(dest_ip)
        for prefix_bits, _, out_link in self._forwarding_table:
            if dest_bin.startswith(prefix_bits):
                return out_link
        return "Default Gateway"


# Optional self-test
if __name__ == "__main__":
    routes = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]
    r = Router(routes)
    test_cases = [
        ("223.1.1.100", "Link 0"),
        ("223.1.2.5", "Link 1"),
        ("223.1.250.1", "Link 4 (ISP)"),
        ("198.51.100.1", "Default Gateway")
    ]
    for ip, expected in test_cases:
        print(f"{ip} -> {r.route_packet(ip)} (expected: {expected})")
