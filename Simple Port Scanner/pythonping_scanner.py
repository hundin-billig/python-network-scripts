#!/usr/bin/env python3
"""
Name: pythonping_scanner_2.py
Author: Lee Dillard
Created: 04/11/2024
Purpose: This program prompts the user to enter a class C address
it uses the Pythonping library to send out ping packets
"""

# Windows: pip install pythonping
# Linux Debian installations:
#   sudo apt update
#   sudo pip3 install pythonping
#   Use sudo to run script: sudo python3 pythonping_scanner.py

from pythonping import ping
# https://docs.python.org/3/library.ipaddress.html
# Convert ip/mask to list hosts

# pip install rich
# Import Console for console printing
from rich.console import Console
# Import Panel for title displays
from rich.panel import Panel
# Initialize rich.console
console = Console()

import ipaddress
import sys

def main():
    display_program_title()

    #-----------------------------SET NETWORK ADDRESS--------------------------#
    """"Set network address x.x.x.x/x or x.x.x.x/x.x.x.x from user"""
    # Change this to the default value of your network
    default_local_network = "192.168.68.1/24"

    # Prompt user to input a network address and press Enter
    # If they press Enter without an network address, the default is used
    network_address = console.input(
        f"[bold white]\n Enter your network address (ex. 10.10.1.0/255.255.252.0): [bold white]"
    ) or default_local_network
    print()

    # Create a network address object from user input
    ip_net = ipaddress.ip_network(network_address, False)

    # Convert all hosts on entered network into a list
    all_hosts = list(ip_net.hosts())
    scan(all_hosts)

#---------------------------------SCAN NETWORK--------------------------------#
def scan(all_hosts: str):
    """Ping all Class C IP addresses 1 - 254"""
    for host_address in all_hosts:
        # Convert the ip address to a string
        ip = str(host_address)
        try:
            # Ping the IP address with two packets
            result = ping(
                ip,                 # Target IP address
                count=1,            # Number of pings
                timeout=2,          # Timeout in seconds
            )

            # If there was a successful ping response
            if result.success():
                # Response time less than 200ms, target is active
                console.print (f"[green]{ip:14}->RTT: {result.rtt_avg_ms:>6.2f} ms[green]")
            else:
                console.print(f"[red]{ip} Inactive[red]")

        except KeyboardInterrupt:
            # Catch the Keyboard Interrupt exception
            console.print(f"[yellow]CTRL-C pressed. Exiting[yellow]")
            sys.exit()

        except Exception as e:
            # Catch all other exceptions
            # Print out the exception error for debugging
            console.print(f"[red]Sorry: {e}[red]")
            sys.exit()         

#---------------------------------DISPLAY PROGRAM TITLE----------------------------#
def display_program_title():
    """Print program title to console"""
    console.print(35 * f"[yellow]-[yellow]")
    console.print(f"[yellow]|      Python Network Ping        |[yellow]")
    console.print(35 * f"[yellow]-[yellow]")
    console.print(f"[bold red]Press CTRL C to exit[bold red]")

# If standalone program, call the main function
# Else, use a module
if __name__ == "__main__":
    main()