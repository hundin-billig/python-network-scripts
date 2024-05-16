"""
Filename: password_checker.py
Author: Lee Dillard
Created: 04/06/2024
Purpose: Crack a password using a plain text password list
https://github.com/danielmiessler/SecLists/tree/master/Passwords
"""

print("+--------------------------------------------------------+")
print("|         -----Lee's Password Checker----                |")
print("|         . . . Use At Your Own Risk . . .               |")
print("+--------------------------------------------------------+")

# Boolean variable to track whether the password has been found
password_found = False

# Get password to get tested from user
input_password = input("Enter the password you want to check: ")

# Enter the password list filename
password_list_file = input("Enter password filename: ")

try:
    # Try to open the password file using the with context handler
    # with automatically closes the file when you exit the block
    with open(password_list_file, "r") as file:

        # Read file --> splitlines() removes \n newline
        # Read each line into a list item

        password_list = file.read().splitlines()

    # The file is automatically closed when with exits

except Exception as e:
    # If there is an error reading the file, we handle it here
    print(f" Error: {e}")
    print(f" {password_list_file} is not found.")
    quit()

#Loop through each password in the password list one at a time
for password in password_list:
    # Compare the input_password with current password in the password_list
    if input_password == password:
        print(f"Password found. The password is {password}")
        password_found = True
        break

# If the password is not found
if password_found == False:
    print(f"Password not found in {password_list_file} file")
    print('\n')
