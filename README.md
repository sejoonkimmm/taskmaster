# taskmaster
42Seoul Outer-circle project

## Summary
The Taskmaster project is a Python-based process management and monitoring system designed for UNIX/Linux systems.
It aims to ensure the reliability and availability of specified processes by automatically starting, stopping, and restarting them according to a set of rules defined in a YAML configuration file.
Key features of Taskmaster include automatic process restarts on failure, detailed event logging, dynamic configuration reloading without affecting running processes, and a simple command-line interface for process control.

The system is designed to be resource-efficient, making it suitable for environments with limited computing capacity.
Although Taskmaster is currently a closed project and not open for external contributions, it welcomes feedback and suggestions from users.

## Overview

Taskmaster is a process management and monitoring system designed to start, supervise, and control a set of configured processes. Inspired by the UNIX/Linux operating system's principles, Taskmaster aims to ensure that specified processes are always running, automatically restarting them if they crash or fail. This tool is particularly useful for managing background tasks and services, ensuring high availability and reliability.

## Features

Process Management: Start, stop, and monitor configured processes.
Automatic Restart: Automatically restart processes based on customizable rules (e.g., always, never, or on unexpected exits).
Logging: Maintain detailed logs of process events (start, stop, restart, crashes).
Configuration Reload: Dynamically reload configuration without stopping the main program or unaffected processes.
Control Shell: Interact with Taskmaster through a simple command-line interface to control and monitor processes.
Minimal Resource Utilization: Designed to run with minimal system resources, making it ideal for environments with limited computing capacity.

## Prerequisites
Python 3.6 or later
'PyYAML' for configuration file parsing.

## Requirements
* Example Connfiguration File:
<img width="885" alt="image" src="https://github.com/sejoonkimmm/taskmaster/assets/117820621/ff588457-faee-470a-a744-b6c0740e9d57">

* Using PyPi
<img width="922" alt="image" src="https://github.com/sejoonkimmm/taskmaster/assets/117820621/0ac3cbeb-a55c-4d91-ab35-197f59160a38">

