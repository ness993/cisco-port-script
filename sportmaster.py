import time  # Importing time for sleep functionality
import os  # Importing os for operating system functionalities
import getpass  # Importing getpass to securely get password input
import logging  # Importing logging for logging purposes
import sys  # Importing sys for system-specific parameters and functions
import argparse  # Importing argparse for command-line argument parsing
import subprocess  # Importing subprocess for executing external commands
import pkg_resources  # Importing pkg_resources to check installed packages
import paramiko  # Importing the paramiko library for SSH connections
from datetime import datetime # Importing the datetime for date


# Clear the screen for Windows before starting the script
os.system('cls' if os.name == 'nt' else 'clear')


"""Main function to execute the script logic."""
    # Argument parser setup
parser = argparse.ArgumentParser(description='Shutdown ports on Cisco devices.')
parser.add_argument('--create-external', action='store_true', help='Create external file with default device data')  # Create external file
parser.add_argument('--file', type=str, help='Path to the external file with device and port list')  # External file path
parser.add_argument('--NOT-DRY-RUN', action='store_true', help='Perform the shutdown operation (default is dry run).')
parser.add_argument('--sleep-time', type=int, default=2, help='Specify sleep time between operations (in ms).') 
parser.add_argument('--log-file', type=str, default='cisco_device_shutdown.log', help='Specify the log file name.')
parser.add_argument('--man', action='store_true', help='Display the manual for using the script')  # Manual option
args = parser.parse_args()  # Parse command-line arguments
# Default valuesS
if args.sleep_time:
    sleep_time = args.sleep_time
else:
    sleep_time = 5
timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
log_file = 'Cisco_Shutdown_Port'
log_exten = ".log"

# Set up logging configuration
logging.basicConfig(
    filename=f'{timestamp}_{log_file}{log_exten}',  # Specify the log file name
    filemode='a',  # Set the file mode to append log entries
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log entry format
    level=logging.INFO  # Set the logging level to INFO
)

def create_external_file(file_path):
    """Create an external file with default device and port data.
    
    Args:
        file_path (str): Path to the file to be created.
    """
    try:
        with open(file_path, 'w') as file:  # Open the file for writing
            file.write("192.168.1.1:GigabitEthernet0/1\n")  # Default device and port
            file.write("192.168.1.2:GigabitEthernet0/2\n")  # Default device and port
            file.write("192.168.1.3:GigabitEthernet0/3\n")  # Default device and port
        log_and_print(f"Created external file: {file_path} with default data.")  # Log file creation
    except Exception as e:  # Catch any exceptions that occur
        log_and_print(f"Error creating file {file_path}: {e}")  # Log the error

def load_devices_from_file(file_path):
    """Load devices from a specified file.
    
    Args:
        file_path (str): Path to the external file containing device details.

    Returns:
        list: A list of dictionaries containing IP addresses and port names.
    """
    devices = []  # Initialize an empty list to store devices
    try:
        with open(file_path, 'r') as file:  # Open the file for reading
            for line in file:  # Loop through each line in the file
                if line.strip():  # Avoid processing empty lines
                    ip, port = line.strip().split(':')  # Split the line into IP and port
                    devices.append({'ip': ip.strip(), 'port': port.strip()})  # Append device info to the list
        log_and_print(f"Loaded devices from {file_path}.")  # Log successful loading of devices
    except Exception as e:  # Catch any exceptions that occur
        log_and_print(f"Error loading devices from file: {e}")  # Log the error
    return devices  # Return the list of devices

def log_and_print(message):
    """Log message and print it to the console.
    
    Args:
        message (str): The message to be logged and printed.
    """
    print(message)  # Print the message to the terminal
    logging.info(message)  # Write the message to the log file

def shut_down_the_port(ip_address_of_device, port_name, username, password, dry_run=True):
    """Connect to a Cisco device and shut down the specified port.
    
    Args:
        ip_address_of_device (str): The IP address of the Cisco device.
        port_name (str): The name of the port to be shut down.
        username (str): The username for SSH authentication.
        password (str): The password for SSH authentication.
        dry_run (bool): If True, perform a dry run without shutting down the port.
    """
    try:
        client = paramiko.SSHClient()  # Create an SSH client instance
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add untrusted hosts
        log_and_print(f"\nConnecting to {ip_address_of_device}...")  # Log connection attempt
        client.connect(ip_address_of_device, username=username, password=password, look_for_keys=False, allow_agent=False)  # Connect to the device
        log_and_print(f"Connected to {ip_address_of_device}.")  # Log successful connection

        remote_connection = client.invoke_shell()  # Start an interactive shell session
        time.sleep(2)  # Wait for the shell to be ready

        log_and_print(f"Entering configuration mode on {ip_address_of_device}...")  # Log entering config mode
        remote_connection.send('configure terminal\n')  # Send command to enter configuration mode
        time.sleep(2)  # Wait for command to execute

        log_and_print(f"Configuring interface {port_name} on {ip_address_of_device}...")  # Log configuring interface
        remote_connection.send(f'interface {port_name}\n')  # Send command to select the interface
        time.sleep(2)  # Wait for command to execute

        if dry_run:  # Check if it is a dry run
            log_and_print(f"*** Dry run: Not shutting down interface {port_name} on {ip_address_of_device}. ***")  # Log dry run message
        else:  # If not a dry run
            log_and_print(f"Shutting down interface {port_name} on {ip_address_of_device}...")  # Log shutting down interface
            remote_connection.send('shutdown\n')  # Send command to shut down the interface
            time.sleep(2)  # Wait for command to execute

        log_and_print(f"Exiting configuration mode on {ip_address_of_device}...")  # Log exiting config mode
        remote_connection.send('end\n')  # Send command to exit configuration mode
        time.sleep(2)  # Wait for command to execute

        if not dry_run:  # If it is not a dry run
            log_and_print(f"Saving the configuration on {ip_address_of_device}...")  # Log saving configuration
            remote_connection.send('write memory\n')  # Send command to save the configuration
            time.sleep(5)  # Wait for the save command to complete

            output = remote_connection.recv(65535).decode('utf-8')  # Receive the command output
            log_and_print(f"\nCommand output from {ip_address_of_device}:\n{output}")  # Log command output
            logging.info(f"Cisco output from {ip_address_of_device}:\n{output}")  # Save output to log

        client.close()  # Close the SSH connection
        log_and_print(f"Connection to {ip_address_of_device} closed.\n")  # Log connection closure

    except paramiko.AuthenticationException:  # Catch authentication errors
        log_and_print(f"Authentication failed for {ip_address_of_device}.")  # Log authentication failure
    except paramiko.SSHException as ssh_exception:  # Catch SSH exceptions
        log_and_print(f"Failed to establish SSH connection to {ip_address_of_device}: {ssh_exception}")  # Log SSH connection failure
    except Exception as e:  # Catch any other exceptions
        log_and_print(f"Error on {ip_address_of_device}: {e}")  # Log the error

def shut_down_ports_on_multiple_devices(devices, username, password, dry_run=True):
    """Shut down ports on multiple Cisco devices, or perform a dry run.
    
    Args:
        devices (list): List of devices to configure.
        username (str): The username for SSH authentication.
        password (str): The password for SSH authentication.
        dry_run (bool): If True, perform a dry run without shutting down ports.
    """
    for device in devices:  # Loop through each device
        time.sleep(sleep_time)  # Sleep between operations to avoid overwhelming the device
        log_and_print(f"\n--- Begining of {device['ip']} ---")
        ip = device['ip']  # Get the device IP address
        port_name = device['port']  # Get the port name
        log_and_print(f"\n--- Processing device {ip} on port {port_name} ---")  # Log device and port processing
        shut_down_the_port(ip, port_name, username, password, dry_run)  # Call the function to shut down the port
        log_and_print(f"\n--- End of {device['ip']} ---")

def display_manual():
    """Display the manual for using the script."""
    manual_text = """
    Cisco Device Port Shutdown Script Manual
    -----------------------------------------
    
    This script allows you to connect to Cisco devices and shut down specific ports. It can perform a dry run 
    to show what would happen without making any changes. Below are the available options and usage instructions.
    
    Usage:
        python script.py [OPTIONS]
    
    Options:
    

        --NOT-DRY-RUN       Production RUN
        --sleep-time        Set sleep timer between devices
        --create-external   Create an external file with default device and port data.
        --file PATH         Specify the path to an external file containing device and port information. 
                            If this option is not used, an internal default list will be used.
        --man               Display this manual.

    External File Format:
    ----------------------
    The external file should contain lines in the following format:
    <IP_ADDRESS>:<PORT_NAME>
    
    Example:
        192.168.1.1:GigabitEthernet0/1
        192.168.1.2:GigabitEthernet0/2
    
    Important Notes:
    -----------------
    - Ensure that you have the necessary permissions to shut down interfaces on the devices.
    - Make sure that SSH access is enabled on the Cisco devices.
    - Use the --dry-run option to verify the commands that will be executed before performing any changes.
    - If using an external file, ensure that it is formatted correctly to avoid errors.

    Logs:
    ------
    All actions taken by the script are logged in a file named 'cisco_device_shutdown.log'.
    This log file contains timestamps and detailed messages about the operations performed.

    Example Usage:
    ---------------
    To shut down ports without making changes (dry run):
        python script.py --dry-run

    To execute the script normally:
        python script.py

    To use an external file:
        python script.py --file /path/to/devices-and-ports.txt

    For installing dependencies:
        python script.py --install

    For checking installed dependencies:
        python script.py --check

    For creating a default external file:
        python script.py --create-external

    """
    log_and_print(manual_text)  # Print the manual text to the console

def main():
    """Main function to execute the script logic."""
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Shutdown ports on Cisco devices.')
    parser.add_argument('--create-external', action='store_true', help='Create external file with default device data')  # Create external file
    parser.add_argument('--file', type=str, help='Path to the external file with device and port list')  # External file path
    parser.add_argument('--NOT-DRY-RUN', action='store_true', help='Perform the shutdown operation (default is dry run).')
    parser.add_argument('--sleep-time', type=int, default=2, help='Specify sleep time between operations (in ms).') 
    parser.add_argument('--log-file', type=str, default='cisco_device_shutdown.log', help='Specify the log file name.')
    parser.add_argument('--man', action='store_true', help='Display the manual for using the script')  # Manual option

    args = parser.parse_args()  # Parse command-line arguments
    
    # Retrieve the log file name
    if args.log_file:
        log_file = args.log_file  # Access the log file value from the parsed arguments
    else:
        log_file='Cisco_Shutdown_Port'
    
    # Retrieve the sleep time
    if args.sleep_time:
        sleep_time = args.sleep_time  # Directly assign sleep time from arguments
        log_and_print(f"User set sleep time between devices to {sleep_time} s")
    else:
        sleep_time = 2
        log_and_print(f"User set sleep time between devices to {sleep_time} s")

    
    
    # Display the manual if --man is specified
    if args.man:
        display_manual()  # Call the function to display the manual
        # Log that the manual was displayed
        log_and_print("Displayed the manual to the user.")  # Log this action
        sys.exit()  # Exit the script gracefully
    
    # Check for --NOT-DRY-RUN argument
    dry_run = True  # Default to dry run
    if len(sys.argv) > 1 and sys.argv[1] == '--NOT-DRY-RUN':
        dry_run = False
        confirmation = input("Are you sure this isn't a dry run? Confirm with 'THIS IS NOT A DRY RUN': ").strip().lower()
        if confirmation != 'this is not a dry run':
            print("Aborting the operation.")
            sys.exit(0)
    
    if dry_run == True:
        log_and_print("Running script as a DRY-RUN")
    else:
        for _ in range(1,3):
            log_and_print("WORNING")
        log_and_print("############################################")
        log_and_print("############# NOT A DRY RUN ################")
        log_and_print("############################################")
        print ("")
        log_and_print("LAST CHANCE TO EXIT")

        
    # Create external file if --create-external is specified
    if args.create_external:
        create_external_file('devices-and-ports.txt')  # Create external file
        sys.exit()  # Exit the script gracefully

    # Load devices from the specified external file or use internal list
    if args.file:
        devices = load_devices_from_file(args.file)  # Load devices from external file
    else:
        # Internal default list of devices if no file is specified
        devices = [
            {'ip': '192.168.1.1', 'port': 'GigabitEthernet0/1'},
            {'ip': '192.168.1.2', 'port': 'GigabitEthernet0/2'},
            {'ip': '192.168.1.3', 'port': 'GigabitEthernet0/3'},
        ]

    # Prompt for username and password
    username = input("Enter your Cisco username: ")  # Get username
    log_and_print(f"User provide a username : {username}")
    password = getpass.getpass("Enter your Cisco password: ")  # Get password securely
    log_and_print(f"User provide a password")

    # Execute the shutdown sequence
    shut_down_ports_on_multiple_devices(devices, username, password, dry_run=dry_run)  # Call function to shut down ports

if __name__ == '__main__':
    main()  # Execute the main function
