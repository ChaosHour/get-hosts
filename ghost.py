#!/usr/bin/env python3

"""
Created on October 16, 2023
By: ChaosHour - Kurt Larsen
Reason: Find FQDNs in your GitHub repo
"""

import re
import os
import sys
from termcolor import colored

def main():
    # Read the directory path and search string from the command line
    if len(sys.argv) < 2:
        print("Usage: python find_fqdns.py <directory> [-s search_string]")
        sys.exit(1)
    directory = sys.argv[1]
    search_string = None
    if len(sys.argv) > 2 and sys.argv[2] == "-s":
        if len(sys.argv) < 4:
            print("Usage: python find_fqdns.py <directory> [-s search_string]")
            sys.exit(1)
        search_string = sys.argv[3]

    # Define the regular expression pattern
    pattern = r"(?i)\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}(?:\.[a-z]{2,})?\b"

    # Loop through the files in the directory and extract the FQDNs
    printed_fqdns = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml") or file.endswith(".pp"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    text = f.read()
                    fqdns = re.findall(pattern, text)
                    for fqdn in fqdns:
                        if fqdn.endswith(".com") or fqdn.endswith(".net") or fqdn.endswith(".org"):
                            if search_string is None or search_string in fqdn:
                                if fqdn not in printed_fqdns:
                                    print(colored("[+]", "green"), fqdn)
                                    printed_fqdns.add(fqdn)
                        else:
                            if search_string is None or search_string in fqdn:
                                if fqdn not in printed_fqdns:
                                    print(fqdn)
                                    printed_fqdns.add(fqdn)

if __name__ == "__main__":
    main()