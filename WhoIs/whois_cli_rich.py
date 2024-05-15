"""
        Name: whois_cli_rich.py
        Author: Lee Dillard
        Created: 04/06/2024
        Purpose: Lookup whois info about web site
	This program can also be used as a module in another program
"""

# https://pypi.org/project/python-whois/

# pip install python-whois
import whois

# pip install rich
# Import Console for console printing
from rich.console import Console
# Import panel for title displays
from rich.panel import Panel

# Initialize rich.console
console = Console()


def main():
    console.print(
        Panel.fit(
            "\n           Domain Whois Information            \n",
            style="bold blue"
        )
    )
    while True:
        domain_name = input("Enter a domain name: ")
        get_who_is(domain_name)
        menu = input("Enter another domain? (y) ")
        if menu.lower() != "y":
            break

#------------------------------GET WHO IS---------------------------------------#
def get_who_is(domain_name):
    """
        Get and display whois info from domain_name parameter
    """
    # Get domain whois information
    d = whois.whois(domain_name)
    print()
    console.print(
        Panel.fit(f"----    {domain_name} Whois Information    ----"),
        style="bold blue"
    )
    print(f"		Expiration Date: {d.expiration_date}")
    print(f"		  Creation Date: {d.creation_date}")
    print(f"		   Updated Date: {d.updated_date}")
    console.print(f"		          Email: {d.emails}")
    console.print(f"		     Nameserver: {d.name_servers}")
    console.print(f"		   Whois Server: {d.whois_server}")
    console.print(f"		Registrant Name: {d.name}")
    console.print(f"		 Registrant Org: {d.org}")
    console.print(f"	       Registrant State: {d.state}")
    console.print(f"	      Registrant Street: {d.address}")
    console.print(f"		 Registrant Zip: {d.city}")
    console. print(f"	     Registrant Country: {d.country}")

# If a standalone program, call the main function
# Else, use a module
if __name__ == "__main__":
    main()
