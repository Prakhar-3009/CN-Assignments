# ip_utils.py
"""
IP utilities: conversion between dotted-decimal IP and 32-bit binary,
and extracting network prefix bits from a CIDR address.
"""

from typing import Tuple

def ip_to_binary(ip_address: str) -> str:
    """
    Convert a dotted-decimal IPv4 address (e.g. "192.168.1.1")
    into a 32-bit binary string (e.g. "11000000101010000000000100000001").
    """
    octets = ip_address.split(".")
    if len(octets) != 4:
        raise ValueError(f"Invalid IPv4 address: {ip_address}")
    binary_parts = []
    for octet in octets:
        num = int(octet)
        if num < 0 or num > 255:
            raise ValueError(f"Invalid octet value: {octet} in {ip_address}")
        binary_parts.append(f"{num:08b}")
    return "".join(binary_parts)


def get_network_prefix(ip_cidr: str) -> str:
    """
    Given a CIDR string like "200.23.16.0/23", return the network prefix bits
    as a binary string (e.g. first 23 bits).
    """
    try:
        ip_part, prefix_len_str = ip_cidr.split("/")
    except ValueError:
        raise ValueError(f"Invalid CIDR notation: {ip_cidr}")
    prefix_len = int(prefix_len_str)
    if prefix_len < 0 or prefix_len > 32:
        raise ValueError(f"Invalid prefix length: {prefix_len}")
    full_bin = ip_to_binary(ip_part)
    return full_bin[:prefix_len]


# Quick manual test when run directly
if __name__ == "__main__":
    print("ip_to_binary('192.168.1.1') ->", ip_to_binary("192.168.1.1"))
    print("get_network_prefix('200.23.16.0/23') ->", get_network_prefix("200.23.16.0/23"))
