```markdown
# Cisco Device Port Shutdown Script

This Python script allows you to connect to multiple Cisco devices over SSH and perform a shutdown operation on specific ports. It includes dry-run functionality, logging, dependency management, and external file support for devices and ports.

## Features

- Connect to Cisco devices via SSH using the same credentials.
- Perform a shutdown operation on specific device ports.
- **Dry-run** mode (default) to simulate actions without actually executing them.
- Option to use an external file for specifying devices and ports.
- Automatic dependency checking and installation.
- Real-time logs of script operations and Cisco device responses.
- Configurable sleep time between device operations.

## Requirements

- Python 3.x
- Paramiko (for SSH connections)

## Installation

### 1. Install the dependencies:

If dependencies like `paramiko` are not installed, the script will prompt you to install them automatically, or you can run the script with the `--install` option:

```bash
python script.py --install
```

Alternatively, you can manually install the dependencies using:

```bash
pip install -r requirements.txt
```

### 2. Clone the Repository:

```bash
git clone https://github.com/your-username/repo-name.git
cd repo-name
```

## Usage

### Basic Usage (Dry Run Mode)

By default, the script runs in **dry-run** mode, where it will simulate the shutdown of ports without making any changes on the Cisco devices:

```bash
python script.py --file devices-and-ports.txt
```

### Performing Actual Shutdown (Non-Dry-Run Mode)

To perform the actual shutdown, you need to explicitly confirm that you're not running a dry-run:

```bash
python script.py --NOT-DRY-RUN
```

Before the script starts, you will be prompted with:

```
Are you sure this isn't a dry run? Confirm with 'THIS IS NOT A DRY RUN':
```

### Creating the External Devices File

You can create an example external file for devices and ports using the `--create-external` option:

```bash
python script.py --create-external
```

This will generate a `devices-and-ports.txt` file in the current directory with example data.

### Using an External File for Devices

If you have a list of devices and ports in an external file, specify it with the `--file` option:

```bash
python script.py --file /path/to/devices-and-ports.txt
```

If no file path is provided, the script will default to using `devices-and-ports.txt` in the current directory.

### Adjusting Sleep Time Between Operations

You can customize the sleep time between device operations using the `--sleep-time` option:

```bash
python script.py --sleep-time 5
```

### Logging

By default, the script logs output to a file with a timestamp. You can specify a custom log file using the `--log-file` option:

```bash
python script.py --log-file custom_log_name.log
```

### Help

To view all available options, use:

```bash
python script.py --help
```

### Manual

To view the detailed manual, run:

```bash
python script.py --man
```

## Options

- `--install`: Install any missing dependencies.
- `--check`: Check if all required dependencies are installed.
- `--create-external`: Create an external `devices-and-ports.txt` file with example data.
- `--file <path>`: Path to an external file with devices and ports.
- `--dry-run`: Perform a dry run (default).
- `--NOT-DRY-RUN`: Perform actual port shutdown.
- `--sleep-time <n>`: Specify the sleep time between device operations (in seconds).
- `--log-file <name>`: Specify the log file name.
- `--man`: Display the script manual.

## Example Device File Format

The external file for devices and ports should have the following format:

```
192.168.1.1, GigabitEthernet0/1
192.168.1.2, GigabitEthernet0/2
```

Each line contains the IP address of the Cisco device followed by the interface/port to be shut down, separated by a comma.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Key Sections:

- **Features**: Lists the key functionalities of the script.
- **Requirements**: Explains the software dependencies.
- **Installation**: Shows how to install dependencies.
- **Usage**: Explains how to run the script in dry-run mode and non-dry-run mode.
- **Logging**: Explains the logging features.
- **Help and Manual**: How to access the help options.
- **Device File Format**: Provides an example of how the external file for devices and ports should be formatted.
- **License**: Mentions the license under which the project is published.

This README will help users understand how to use your script effectively on GitHub.
