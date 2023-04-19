import csv
import os
import re
import sys
from collections import Counter

from colorama import Fore, Style

GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
NORMAL = Style.RESET_ALL


def parse_smtp_logs(log_file, results_file):
    """Parse the log file from a Microsoft IIS SMTP server and return the results in a csv file.

    Args:
        log_file (str): Full UNC path for the log file to parse.
        results_file (str): Full UNC path for the csv results file.  Fields are: hostname, IP address and the count of occurrences in the log file.
    """
    ro = re.compile(
        r"""
                    (?P<date>^\d{4}[\-\d{2}]+)\s     # Date (YYYY-MM-DD)    
                    (?P<time>[\d{2}:]+)\s            # Time (HH:MM:SS)
                    (?P<ip>[\d{1,3}\.]+)\s           # Source IP Address
                    (?P<host>[\S]+)                  # Source Hostname
                    """,
        re.X,
    )

    host_list = []

    with open(log_file) as f:
        for line in f:
            if m := ro.search(line):
                if not m["host"].startswith("Outbound"):
                    host_list.append((m["host"], m["ip"]))

    host_count = Counter(host_list)

    with open(results_file, "w") as f:
        writer = csv.writer(f)
        header = ["HOSTNAME", "IP ADDRESS", "COUNT"]
        writer.writerow(header)
        for host, count in host_count.items():
            writer.writerow([f"{host[0]}", f"{host[1]}", f"{count}"])

    input(f"{GREEN}Press any key to exit...{NORMAL}")


def main():
    print(f"\n{YELLOW}######################################{NORMAL}")
    print(f"{YELLOW}# MICROSOFT IIS SMTP LOG FILE PARSER #{NORMAL}")
    print(f"{YELLOW}######################################{NORMAL}\n")
    log_file_name = input(
        f"{YELLOW}Enter the full path for a log file to parse: {NORMAL}"
    )
    results_file_name = input(
        f"{YELLOW}Enter the full path for the csv results file: {NORMAL}"
    )

    if os.path.exists(log_file_name):
        parse_smtp_logs(log_file_name, results_file_name)
    else:
        print(f"{RED}File {log_file_name} not found.{NORMAL}")
        input(f"{RED}Press any key to exit...{NORMAL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
