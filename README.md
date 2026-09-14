# Telegram-Based-Remote-Administration-Tool-RAT

A Python-based Telegram bot for remote computer administration, system monitoring, and security research. The project integrates Telegram Bot API with system-level utilities to provide remote control, file management, hardware monitoring, and Windows-specific functionality.

**Author:** 0xplt Aditya Bhosale

**Version:** 3.2 — Enhanced Bomb Edition

## Features

### Remote System Monitoring

* System information including operating system, hostname, CPU, RAM, disk usage, and local IP.
* Running process enumeration with PID, process name, and memory usage.
* Active window monitoring on Windows.
* Clipboard access and background clipboard change logging.
* IP-based geolocation including public IP, country, region, city, ISP, and coordinates.

### Screen and Input Automation

* Capture and send desktop screenshots through Telegram.
* Move the mouse to specified screen coordinates.
* Perform left, right, and middle mouse clicks.
* Type text remotely using PyAutoGUI.

### File Management

* Upload files from the computer to Telegram.
* Download documents from Telegram and save them to the working directory.
* Search for files by filename pattern.
* File search returns up to 10 matching results.

### Hardware Access

* Capture a photo using the default webcam.
* Record and send 5-second audio recordings.
* Collect basic system and hardware information.

### Keylogger

* Start and stop keyboard event logging.
* Record keystrokes to `keylog.txt`.
* Retrieve stored keystroke logs through Telegram.
* Clear the keylog after retrieval.

### Windows System Features

* Add the bot to Windows startup using the current user's Run registry key.
* Remove the startup entry.
* Hide the console window.
* Display a startup notification popup.
* Shutdown and restart the computer with a 10-second delay.

### Enhanced Bomb Feature

A demonstration feature that displays a fullscreen cyberpunk-themed popup with animated Matrix-style text, glitch effects, a countdown timer, and temporary input blocking.

* Fullscreen topmost window.
* Matrix rain animation.
* Glitch-style text effects.
* 10-second countdown.
* Automatic window closure and input restoration.

This feature is intended for controlled demonstrations on a dedicated test machine.

### Telegram Bot Interface

* Telegram command-based remote administration.
* User ID authentication for command access.
* `/start`, `/help`, and `/about` commands.
* Logging to `bot_debug.log`.
* Background monitoring threads for clipboard and Windows active-window tracking.
* `/stop` command to terminate the bot and monitoring components.

## Technology Stack

| Technology          | Purpose                                   |
| ------------------- | ----------------------------------------- |
| Python 3            | Core programming language                 |
| python-telegram-bot | Telegram bot framework                    |
| PyAutoGUI           | Screen capture and input automation       |
| psutil              | System information and process monitoring |
| pynput              | Keyboard event handling                   |
| OpenCV              | Webcam capture                            |
| sounddevice         | Audio recording                           |
| SciPy               | WAV audio file creation                   |
| Pyperclip           | Clipboard access                          |
| Requests            | IP geolocation API requests               |
| Tkinter             | Graphical demonstration window            |
| Windows Registry    | Startup configuration                     |

## Project Structure

```text
telegram-remote-pc/
├── remote_pc.py
├── requirements.txt
├── README.md
├── bot_debug.log
├── keylog.txt
├── clipboard_log.txt
└── window_log.txt
```

The Python script contains the Telegram handlers, system utilities, background monitoring functions, and demonstration interface.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd telegram-remote-pc
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install python-telegram-bot pynput pyautogui psutil opencv-python sounddevice scipy pyperclip requests
```

Tkinter is required for the graphical demonstration. On Windows it is normally included with Python.

### 4. Configure the bot

Create a Telegram bot using BotFather and configure the bot token and authorized Telegram user ID through environment variables.

```powershell
$env:BOT_TOKEN = "your_bot_token"
$env:ALLOWED_USER_ID = "your_telegram_user_id"
```

Do not commit bot tokens, credentials, or private configuration to the repository.

### 5. Run the application

```bash
python remote_pc.py
```

The bot starts polling Telegram for commands and initializes the supported monitoring components.

## Command Reference

| Command               | Description                          |
| --------------------- | ------------------------------------ |
| `/start`              | Display the bot command menu         |
| `/help`               | Display help                         |
| `/about`              | Show project information             |
| `/screenshot`         | Capture a desktop screenshot         |
| `/keylog_start`       | Start keyboard event logging         |
| `/keylog_stop`        | Stop keyboard event logging          |
| `/keylog_get`         | Retrieve and clear keylog data       |
| `/shell <cmd>`        | Execute a system command             |
| `/upload <filepath>`  | Send a file to Telegram              |
| `/download`           | Receive and save a Telegram document |
| `/sysinfo`            | Display system information           |
| `/mouse <x> <y>`      | Move the mouse                       |
| `/click <button>`     | Perform a mouse click                |
| `/type <text>`        | Type text                            |
| `/webcam`             | Capture a webcam photo               |
| `/record`             | Record 5 seconds of audio            |
| `/clipboard`          | Retrieve clipboard contents          |
| `/activewindow`       | Show the active window               |
| `/processes`          | List running processes               |
| `/shutdown`           | Schedule a system shutdown           |
| `/restart`            | Schedule a system restart            |
| `/findfile <pattern>` | Search for matching files            |
| `/location`           | Retrieve IP-based geolocation        |
| `/startup`            | Add Windows startup entry            |
| `/remove_startup`     | Remove Windows startup entry         |
| `/bomb`               | Launch the cyberpunk demonstration   |
| `/stop`               | Stop the bot                         |

## Architecture

The project uses an event-driven Telegram bot with background monitoring threads.

```text
                    Telegram User
                          |
                          v
                   Telegram Bot API
                          |
                          v
                Python Bot Application
                          |
             +------------+-------------+
             |            |             |
             v            v             v
       Authentication  Commands    Background
       & Logging       Handlers    Monitoring
             |            |             |
             |            v             |
             |       System Utilities   |
             |            |             |
             +------------+-------------+
                          |
                          v
                    Local Computer
```

### Main Components

* **Authentication:** Validates the Telegram user's ID before executing commands.
* **Command handlers:** Connect Telegram commands to Python functions.
* **System utilities:** Provide monitoring, file operations, input automation, and hardware capture.
* **Background threads:** Monitor clipboard changes and active-window changes.
* **Logging:** Records bot events and errors in `bot_debug.log`.

## Security Considerations

This project demonstrates capabilities that can also be abused as spyware or remote-access malware. Use it only on systems you own or have explicit permission to administer.

The current implementation has important limitations:

* The bot token must be protected and rotated if exposed.
* Telegram user ID authentication is a single-factor access control and does not replace strong authentication.
* Shell execution accepts arbitrary commands and should not be exposed to untrusted users.
* Keystroke, clipboard, webcam, and audio collection require explicit consent and appropriate privacy controls.
* Startup persistence and hidden execution should be disabled unless required for an authorized lab.
* The bomb demonstration should be tested only on a dedicated machine with input-blocking recovery procedures.

## Learning Objectives

This project provides hands-on experience with:

* Python automation and asynchronous programming.
* Telegram Bot API integration.
* Operating system interaction and process management.
* Windows registry and startup behavior.
* Hardware access through Python libraries.
* Background threading and event-driven design.
* Authentication and remote administration security.
* Security risks associated with excessive remote privileges.

## Future Improvements

* Implement role-based access control and stronger authentication.
* Replace arbitrary shell execution with an allowlisted command set.
* Add command audit logs and rate limiting.
* Use encrypted configuration management and secret rotation.
* Add explicit consent and privacy controls for sensitive hardware features.
* Implement safe shutdown cancellation and reliable background-thread cleanup.
* Add unit tests and a dedicated security testing mode.
* Improve cross-platform support for Windows and Linux.
* Add a web dashboard for authorized system monitoring.

## License

This project is intended for educational and authorized security research. Use it only on systems where you have permission to perform remote administration or testing.

---

**Built by 0xplt Aditya Bhosale**
