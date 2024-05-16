#!/usr/bin/env python3
"""
Filename: nmap_ping_scan_gui.py
Author: Lee Dillard
Created: 02/17/2024
Purpose: Use Python nmap wrapper to scan network
"""

from tkinter import *
from tkinter.ttk import *
# Windows: pip install python-nmap
# Linux: sudo pip3 install python-nmap
import nmap

class NmapScanner:
	
	def __init__(self):
		"""Initialize program"""
		self.window = Tk()
		self.window.title("nmap App")
		self.window.geometry("525x600")
		self.window.config(padx=10, pady=10)
		
		self.create_widgets()
		self.create_treeview()
		mainloop()
	
	def scan(self, *args):
		# Return a list of tuples from treeview
		items = self.tree.get_children()
	
		# Iterate through list to delete all items in the treeview
		for item in items:
			self.tree.delete(item)
	
		# Initialize create Nmap port scanner object
		nm = nmap.PortScanner()
		self.network = self.entry_network_address.get()
		# Set target and arguments
		# You can get common settings from Zenmap
		# -sn - Ping scan
		nm.scan(
			hosts=self.network,
			arguments="-sn"
		)

		num_hosts = 0
		for hosts in nm.all_hosts():
			# Get scan information from nmap dictionary
			host = nm[hosts].get("addresses").get("ipv4")
			state = nm[hosts].get("status").get("state")
			mac_address = nm[hosts].get("addresses").get("mac")
			# If the device does not have a MAC address
			# it will not have a MAC vendor.
			try: 
				mac_vendor = list(nm[hosts].get('vendor').values()) [0]
			except:
				# If there isn't a MAC address or the MAC address lookup
				# fails, leave it empty
				mac_vendor = ""
			
			self.tree.insert("", "end", text=num_hosts, values=(
				host, state, mac_address, mac_vendor)
			)
			num_hosts += 1
		
		# Get scan statistics
		scan_stats = nm.scanstats()
		self.lbl_hosts_value.config(text=f"Hosts: {num_hosts}")
		self.lbl_elapsed_value.config(
			text=f"Elapsed: {scan_stats.get ('elapsed')} seconds")
	
	def create_widgets(self):
		"""Create and place GUI widgets"""
		# Create widgets
		# Create frames
		self.entry_frame = LabelFrame(self.window, text="Network Address")
		self.display_frame = LabelFrame(self.window, text="Ping Scan")
	
		# Fill the frame to the width of the window
		self.entry_frame.pack(fill=X)
		self.display_frame.pack(fill=X)
		# Keep the frame size regardless of the widget sizes
		self.entry_frame.pack_propagate(False)
		self.display_frame.pack_propagate(False)
	
		self.entry_network_address = Entry(self.entry_frame, width=40)
		# Set this to your default network address
		self.entry_network_address.insert(
			END, string="192.168.0.1/0")
		# Select all text in entry
		self.entry_network_address.selection_range(0, END)
		self.entry_network_address.focus_set()
	
		self.btn_scan = Button(
			self.entry_frame,
			text="Ping Scan",
			command=self.scan
		)
	
		self.lbl_hosts_value = Label(self.display_frame, text="Hosts:")
		self.lbl_elapsed_value = Label(self.display_frame, text="Elapsed:")
	
		# Enter key will activate the scan method
		self.window.bind('<Return>', self.scan)
		self.window.bind('<KP_Enter>', self.scan)
	
		# Place widgets
		self.entry_network_address.grid(
			row=1, column=1, columnspan=2, sticky=W)
		self.btn_scan.grid(row=1, column=3)
	
		self.entry_frame.pack_configure(padx=5, pady=5)
		self.display_frame.pack_configure(padx=5, pady=5)
		# Set padding for all widgets
		for child in self.entry_frame.winfo_children():
			child.grid_configure(padx=5, pady=5)
		for child in self.display_frame.winfo_children():
			child.grid_configure(padx=5, pady=5)

	def create_treeview(self):
		"""Setup tree view for display"""
		# Create treeview
		self.tree = Treeview(
			self.display_frame,
			height=20,
			columns=("ip", "state", "mac", "vendor"),
			style="Treeview",
			show="headings",
			selectmode = "browse"
		)
	
		# Setup the columns
		self.tree.column("ip", width=100)
		self.tree.column("state", width=25)
		self.tree.column("mac", width=120)
		self.tree.column("vendor", width=225)
	
		# Setup the heading text visible at the top of the column
		self.tree.heading("ip", text="IP", anchor=W)
		self.tree.heading("state", text="", anchor=W)
		self.tree.heading("mac", text="MAC", anchor=W)
		self.tree.heading("vendor", text="Vendor", anchor=W)
	
		# Grid the tree
		self.tree.grid(row=0, column=0)
	
		# Create scrollbar for treeview
		self.scrollbar = Scrollbar(
			self.display_frame,
			orient="vertical",
			command=self.tree.yview
		)
	
		# Set scrollbar to scroll vertically and attach to the tree
		self.tree.configure(yscroll=self.scrollbar.set)
	
		# Grid scrollbar just to the right of the tree
		# sn (SouthNorth) expands scrollbar to height of tree
		self.scrollbar.grid(row=0, column=1, sticky="sn")
	
# Create program object
nmap_scanner = NmapScanner()
