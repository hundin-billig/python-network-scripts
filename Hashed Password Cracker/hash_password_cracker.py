#!/usr/bin/env python3
"""
    Name: hash_password_cracker.py
    Author: Lee Dillard
    Created: 04/17/2024
    Purpose: Crack a hashed password using a dictionary attack with a wordlist file
"""

import hashlib

#---------------PRINT TITLE-----------------------#
def print_title():
    print("+-------------------------------------------------------------+")
    print("+    --        Lee's Best Hashed Password Cracker        --   +")
    print("+              Demonstrating a dictionary attack              +")
    print("+                   Use at your own risk                      +")
    print("+-------------------------------------------------------------+")

#---------------------HASH SHA256--------------------#
def hash_sha256(password: str) -> str:
    """Pass in a plain text password, return a hashed string using sha256.

    Hash a plain text password with the sha256 hashing algorithm.
    sha256 is currently considered a secure hashing algorithm.

    Args:
        password: A plain text password is a string

    Return:
        hashed_digest: A hexidecimal string representation 
        of the binary hashed password. This is called a digest.
    """

    # Encode the password string to binary
    encoded_password = password.encode()
    # Hash the password with md5
    hashed_password = hashlib.sha256(encoded_password)
    # A hexidecimal string representation of the binary hashed password
    hashed_digest = hashed_password.hexdigest()
    return hashed_digest

#-----------------OPEN FILE---------------------#
def open_file(word_list_file: str) -> list[str]:
    """Open specified file, return word list"""
    try:
        # Try to open the password file using the with context handler
        # with automatically closes the file when you exit the block
        # Some word lists have some characters that cause issues,
        # Use the parameter errors="ignore"
        with open(word_list_file, "r", errors="ignore") as file:
            # Read file --> splitlines() removes \n newline
            # Read each line into a list item
            word_list = file.read().splitlines()
        # The file is automatically closed

    except Exception as e:
        # If there is an error reading the file, we handle it here
        print(f"Error: {e}")
        print(f"{word_list_file} is not found.")
        quit()
    else:
        return word_list

#-----------------------MAIN----------------------#
def main():
    print_title()
    # Boolean variable to track whether or not the password has been found
    password_found = False

    input_password = input("Enter a password: ")

    # Hash input password with sha256. This simulates what you would
    # capture if you captured a password authentication hash over a network
    captured_hash = hash_sha256(input_password)

    # Display the simulated hash to find in our word list file
    print(f"Captured hash to find: {captured_hash}")

    word_list_filename = input("Enter password filename: ")
    # Call open_file function to open word list.
    # Return list of words to hash to compare
    word_list = open_file(word_list_filename)

    # Loop through each password in the word list one at a time
    # Compare the hashed_password with the hashes of each password
    # in the password file
    for password in word_list:
        # Hash a dictionary list word into SHA256 hash
        password_hash = hash_sha256(password)

        # Compare hash from dictionary list to captured hash
        if password_hash == captured_hash:

            print(f"Password found. \nThe password is: {password}")
            password_found = True
            break

    # If the password is not found
    if password_found == False:
        print(f"Password not found in {word_list_filename} file")


# If standalone program, call the main function
# Else, use as a module
if __name__ == "__main__":
    main()
