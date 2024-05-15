"""
Filename: port_scanner_threaded.py
Author: Lee Dillard
Created: 04/26/2024
Purpose: This program prompts the user to enter network address
it uses the pythonping library to detect active devices
at each possible IP address in the range
"""

# pip install rich
# Import Console for console printing
from rich.console import Console
# Import Panel for title displays
from rich.panel import Panel
# Initialize rich.console
console = Console()

import threading
import queue 
import time 

# https://docs.python.org/3/library/ipaddress.html
# Convert ip/mask to list of hosts
import ipaddress
# pip install pythonping
from pythonping import ping

class PythonPingScanner():
    def __init__(self):
        console.print(
            Panel.fit(
                "    Threaded Network Scanner    ",
                style="bold red",
                subtitle="By Lee Dillard")
        )
        # Define a thread lock to prevent threads running into each other
        self.thread_lock = threading.Lock()

        # Create thread queue to keep track of the threads
        self.q = queue.Queue()

        # Define number of threads
        self.NUMBER_OF_THREADS = 254

        # Initialize live hosts count
        self.hosts_count = 0

        # Store the scan results
        self.active_hosts = []


        #print("+--------------------------------------+")
        #print("|       Threaded Network Scanner       |")
        #print("+--------------------------------------+")

        self.get_network_address()
        self.start_scan()

#-------------------GET NETWORK ADDRESS-----------------#
    def get_network_address(self):
        """Get network address x.x.x.x/x or x.x.x.x/x.x.x.x from user"""
        #------------------FIND NETWORK ADDRESS----------------#
        # Use ipconfig in Windows, ifconfig in Linux
        # to find your local network address
        # Example: if your IP address is 
        # 192.168.1.1
        # Subnet mask: 255.255.255.0
        # your network address is 192.168.1.0/24
        # If your subnet mask is different than 255.255.255.0
        # Type in the subnet mask directly: 192.168.10.0/255.255.252.0

        # Change this to the default value of your network
        default_local_network = "192.168.68.0/22"

        # Prompt the user to input a network address and press Enter
        # If they press Enter without a network address, the default is used
        network_address = console.input(f"[bold white]Enter network address (ex. 192.168.1.0/24):[bold white] "
        ) or default_local_network

        console.print(f"\n[green]Pinging: {network_address}[green]")

        # Create a network address object from user input
        ip_net = ipaddress.ip_network(network_address)

        # Convert ip_net address object list into a list of all valid hosts
        self.all_hosts = list(ip_net.hosts())

        # For debugging
        #print(self.all_hosts)

#-------------------START SCAN----------------#
    def start_scan(self):
        # Store start time of program scan execution
        start_time = time.time()

        # Create /spawn multiple threads
        for r in range(self.NUMBER_OF_THREADS):

            # Set the thread target method
            thread = threading.Thread(target=self.worker)

            # All threads end when main program ends for cleaner shutdown
            thread.daemon = True

            # Start/spawn the thread
            thread.start()

        # Put all task requests into the queue
        for host in self.all_hosts:
            self.q.put(str(host))

        # Block program from continuing
        # until all worker tasks are complete in the queue
        self.q.join()

        # Calculate elapsed time
        scan_time = time.time() - start_time

        # Print number of hosts and time scan took to complete
        console.print(
            f"[bold white]{self.hosts_count} hosts are live[bold white]")
        console.print(
            f"[bold yellow]Run Time: {round(scan_time, 2)} sec[bold yellow]")
        print()
        self.print_sorted_results()

#-----------------------THREAD WORKER----------------------#
    def worker(self):
        """This method does all the work"""
        while True:
            # Get the next IP address from the queue
            host = self.q.get()

            # Scan the IP address
            self.scan(host)

            # Worker announces the tssk is done, task is removed from queue
            self.q.task_done()

#--------------------SCAN NETWORK------------------#
    def scan(self, ip):
        """Ping all IP addresses"""
        try:
            # Ping the IP address with two packets
            result = ping(
                ip,              # Target IP address
                count=2,         # Number of pings
                timeout=2        # Timeout in seconds
            )

            # If there is a successfull ping
            if result.success():
                # Thread_lock prevents the threads from running into each other
                with self.thread_lock:

                    # Track count of live hosts
                    self.hosts_count += 1
                    self.active_hosts.append((ip, result.rtt_avg_ms))
                    # Response time less than 2000ms, target is active
       
        except Exception as e:
            # Catch all exceptions
            # Print out the exceptions error for debugging
            console.print(f"[red]Sorry: {e}[\red]")

#------------------------------------SORTED RESULTS--------------------------------#
    def print_sorted_results(self):
        # Print the results by active hosts IP address
        self.active_hosts.sort(key=lambda x: ipaddress.ip_address(x[0]))
        for ip, rtt in self.active_hosts:
            console.print(f"[bold blue]{ip:14}[bold blue][red]  -> RTT:  {rtt:<6.2f} ms[red]")

# Create program object to start program
python_ping_scanner = PythonPingScanner()
while True:
    menu = console.input(f"[bold white]Another scan (Y/N):[bold white]").lower()
    if menu == "n":
        break
    python_ping_scanner.start_scan()
