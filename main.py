"""
Name: Juliana Oyola-Pabon
Date:10/02/2023
Assignment:Module 8: Send Authenticated Message
Due Date:10/15/2023
Solve a simple programming problem based on various approaches to computer security and information management.
Build a small scale real-world application that incorporates the principles of secure computing including cryptography,
network security, and data protection.
All work below was performed by Juliana Oyola-Pabon """
import platform
import subprocess
import time

# this page runs all the main programs - Runs DBs first - the Server  then the site logic


# Run setup.py first
subprocess.run(["python", "site/patientDB.py"])

# Runs testResult DB
subprocess.run(["python", "site/testResultDB.py"])

import threading
import subprocess

# Function to run server.py
def run_server():
    subprocess.run(["python", "site/startServer.py"])


# Function to run site.py
def run_site():
    subprocess.run(["python", "site/patientSite.py"])


# Create threads for running server and site scripts
server_thread = threading.Thread(target=run_server)
site_thread = threading.Thread(target=run_site)

# Start both threads
server_thread.start()
site_thread.start()

# Wait for threads to complete (optional)
server_thread.join()
site_thread.join()
