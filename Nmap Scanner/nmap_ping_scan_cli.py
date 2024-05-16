#!/usr/bin/env python3
"""
Filename: nmap_ping_scan_cli.py
Author: Lee Dillard
Created: 02/17/2024
Purpose: Use Python nmap wrapper to scan network
"""

# Windows: pip install python-nmap
# Linux: sudo pip3 install python-nmap
import nmap

def main():
	print(" +--------------------------------------------------------+")
	print(" ------         Python nmap Network Scanner         ------+")
	print(" +--------------------------------------------------------+")
	
	# Change to default value of your network
	local_network = "192.168.68.1/24"
	# Get network address, if blank use local_network
	network = input (
		"Enter network address (for ex. 192.168.1.0/24): ") or local_network
	scan(network)
	
def scan(network):
	"""Create Nmap port scanner object"""
	nm = nmap.PortScanner()
	
	print(f" Nmap Version: {nm.nmap_version()}")
	print(f" Scanning the network...")
	
	# Set target and arguments
	# You can get common settings from Zenmap
	# -sn - Ping scan
	nm.scan(
		hosts=network,
		arguments="-sn"
	)
	
	# Counter to track which host we are scanning
	num_hosts = 0
	for host in nm.all_hosts():
		# Loop through all hosts one at a time
		# Get scan information from nmap dictionary
		host = nm[host].get("addresses").get("ipv4")
		state = nm[host].get("status").get("state")
		# Display the host IP and status
		print(f" {host} \t{state}")
		num_hosts += 1
		
	print(f"Number of hosts: {num_hosts}")
	# Get and display scan statistics
	scan_stats = nm.scanstats()
	print(f"Elapsed: {scan_stats.get('elapsed')} seconds\n")
	
if 	__name__ == '__main__':
	main()
