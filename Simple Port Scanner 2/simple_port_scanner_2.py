#!/usr/bin/python3
"""
Filename: simple_port_scanner_2.py
Author: Lee Dillard
Created: 04/23/2024
Purpose: Scans each port with a connection attempt
"""

import queue
import socket
import time
import threading
import rich
# Windows: pip install rich
# Linux: pip3 install rich

# Import Console for base console printing
from rich.console import Console
# Import Panel for title displays
from rich.panel import Panel
# Initialize rich.console
console = Console()

class PortScanner:

    def __init__(self):
        # Print program title using rich.panel
        console.print(
            Panel.fit("      Fast Port Scanner      ",
                    style="bold blue",
                    subtitle="By Lee Dillard")
        )
    
        # Set a default socket connection timeout of .25 seconds
        socket.setdefaulttimeout(0.5)   
        self.thread_lock = threading.Lock()
        self.ports = queue.Queue()
        self.num_threads = 200 
        target_host = input("Enter the host name/IP to be scanned: ")
        # Get the IP address of the host
        self.target_ip = socket.gethostbyname(target_host)
        print(f"Starting port scan on host: {self.target_ip}")
        self.start_time = time.time()
        self.count = 0
        # Scan the first 5000 ports maximum ports 65535
        port_range = 5001
        for port in range(1, port_range):
            self.ports.put(port)
        
#------------------------------SCAN PORT--------------------#
    def scan_port(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((self.target_ip, port))
            if result == 0:
                # Thread_lock prevents the threads from
                # running into each other
                with self.thread_lock:
                    self.count += 1
                    console.print(f"[green] [+] Port {port}: OPEN[/green]")
            s.close()
        except:
            pass

#------------------WORKER--------------#
    def worker(self):
        while not self.ports.empty():
            port = self.ports.get()
            self.scan_port(port)
#--------------------RUN------------------#
    def run(self):
        threads = []
        for i in range(self.num_threads):
            t = threading.Thread(target=self.worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        scan_time = time.time() - self.start_time
        print(f"{self.count} ports open.")
        print(f"Time taken: ({round(scan_time, 2)})sec")

scanner = PortScanner()
scanner.run()