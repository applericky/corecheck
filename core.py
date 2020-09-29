#!/usr/bin/python3
import concurrent.futures
import time
import platform
import subprocess
# from .pypiupdate import *
import argparse
import sys

__version__ = "20200929"


def ping_task(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    ping = ["ping", param, "3", host]
    ping_return_code = subprocess.run(
        ping, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if ping_return_code.returncode == 0:
        print(host + " is up")
    else:
        if ping_return_code.returncode == 2:
            print(host + " is down")


def make_hosts(site_number):
    return [
        site_number + ".apple.com",
        site_number + ".icloud.com",
        site_number + ".github.com",
        site_number + ".microsoft.com",
        site_number + ".reddit.com",
    ]


def vis(site_number):
    return [
        site_number + ".google.com",
    ]


def vis_scan():
    try:
        site_number = input("Please enter site number: ")
        thread_worker(vis(site_number))
    except KeyboardInterrupt:
        exit("\nApp exited!")

    cont = True
    while cont == True:
        try:
            if not input("Do another scan? [Y/n]: ").lower() in ["y", "yes"]:
                cont = False
                exit()
            else:
                site_number = input("Please enter site number: ")
                thread_worker(vis(site_number))
        except KeyboardInterrupt:
            exit("\nApp exited!")


def scan():
    try:
        site_number = input("Please enter site number: ")
        thread_worker(make_hosts(site_number))
    except KeyboardInterrupt:
        exit("\nApp exited!")

    cont = True
    while cont == True:
        try:
            if not input("Do another scan? [Y/n]: ").lower() in ["y", "yes"]:
                cont = False
                exit()
            else:
                site_number = input("Please enter site number: ")
                thread_worker(make_hosts(site_number))
        except KeyboardInterrupt:
            exit("\nApp exited!")


def thread_worker(hosts_list):

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        for host in hosts_list:
            executor.submit(ping_task, host)


def main():
    formatter_class = argparse.RawDescriptionHelpFormatter

    parser = argparse.ArgumentParser(formatter_class=formatter_class)
    parser.add_argument(
        "-u",
        "--update",
        dest="update",
        action="store_true",
        help="Update script from pypi",
    )

    parser.add_argument(
        "-hy",
        "--hype",
        dest="vis",
        action="store_true",
        help="Ping hypervisors devices",
    )

    args = parser.parse_args()
    # Check for updates
    if args.update:
        PypiUpdater("core", force_update=True)
    if args.vis:
        vis_scan()
    if len(sys.argv) == 1:
        scan()


if __name__ == "__main__":
    main()
