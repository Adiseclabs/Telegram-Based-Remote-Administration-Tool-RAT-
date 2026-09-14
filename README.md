# Telegram-Based Remote Administration Tool (RAT) — Authorized Self-Owned Windows Lab

A personal cybersecurity lab project for learning remote administration concepts on a Windows machine you own.

> **Status:** Educational prototype / personal lab only.  
> **Platform:** Windows 10/11  
> **Language:** Python 3.9+

---

## ⚠️ Disclaimer

This project is for **educational and authorized personal lab use only**.

It must only be run on systems you own or have explicit written permission to test.  
Unauthorized access, surveillance, or control of any device is illegal and unethical.  
The author assumes no liability for misuse.

**Do not deploy this on shared, corporate, or third-party devices.**

---

## Ethical Scope

This project is intentionally limited to safe, transparent administration tasks:

- Self-owned Windows device only
- Visible actions only
- No covert surveillance
- No keylogging
- No webcam or audio capture
- No clipboard logging
- No hidden persistence
- No remote shell
- No fake ransomware or screen takeover
- All actions must be consented to and auditable

---

## Project Overview

A Python-based Telegram bot for remote administration of a personally owned Windows machine.  
It demonstrates authenticated command handling, system telemetry, and basic diagnostics.

This is a learning project for secure remote administration — not a production tool.

---

## Features (Sanitized)

- Telegram bot authentication with allowlisted user ID
- System information: OS, CPU, RAM, disk
- Process list
- Screenshot capture with visible notification
- File upload/download for diagnostics
- Basic automation for accessibility testing
- Local audit logging

---

## Removed / Not Included

The following features are intentionally excluded because they are dangerous or privacy-invasive:

- Keylogger
- Webcam capture
- Audio recording
- Clipboard monitoring
- Hidden console
- Startup persistence
- Remote shell
- Fake ransomware / “bomb” / screen takeover

If you need these features, this project is not for you.

---

## Architecture

```text
.
├── bot.py              # Telegram handlers and command routing
├── monitor.py          # System telemetry
├── actions.py          # Safe automation and diagnostics
├── config.py           # Loads token and allowlisted user ID
├── logs/               # Local audit logs
├── requirements.txt
└── README.md
