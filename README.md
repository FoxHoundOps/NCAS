# 🛰️ NCAS - Network Capture and Archiver Scripts

**NCAS (Network Capture and Archiver Scripts)** is a lightweight and interactive toolkit designed to automate the scheduling and management of recurring network traffic captures using `dumpcap`. It also includes a companion script for organizing and compressing `.pcap` files into zip archives for easier storage and management.

This project is ideal for system administrators, network defenders, or security professionals who need repeatable, scheduled traffic capture with built-in archival handling.

---

## 📁 Contents

- `generate_cronjob_capture.py`  
  Interactive Python script that walks users through scheduling recurring packet captures using `cron`, including automatic creation of daily directories and zipping logic.

- `archiver.sh`  
  Bash script that traverses a given directory recursively, identifies `.pcap` files, and compresses them into `.zip` files if not already archived.

---

## 🚀 Quick Start

### Requirements

- Python 3.6+
- `dumpcap` (part of the Wireshark suite)
- `zip` utility
- Linux/macOS shell
- Permissions to run `dumpcap` (e.g., `sudo` or using `setcap`)

---

### 📦 Usage

#### 1. Generate Cronjobs for Packet Capture

```bash
python3 generate_cronjob_capture.py
```

This will prompt you to enter:
- Interface number (as listed by `dumpcap -D`)
- Start and end dates
- Daily capture start time (24hr format)
- Capture duration in hours
- Split size for `.pcap` files (in KB)
- Base filename and output directory
- Time to run the archiver script
- Optionally initialize daily subdirectories and copy `archiver.sh` to the target path

At the end, the script outputs a list of `cron` entries. Example:

```bash
00 02 15 07 * dumpcap -P -i eth0 -a duration:3600 -b filesize:100000 -w /opt/pcaps/day1/capture_day1.pcap
30 03 * * * /opt/pcaps/archiver.sh /opt/pcaps/ >> /opt/pcaps/archiver_error_log.txt 2>&1
```

Paste these into your crontab using `crontab -e`.

---

#### 2. Archive `.pcap` Files

```bash
./archiver.sh /path/to/pcaps/
```

The script:
- Iterates through all subdirectories of the given path
- Identifies `.pcap` files
- Creates `.zip` archives only for `.pcap`s that are not yet zipped

---

## 📂 Directory Structure Example

When setting up a capture session over multiple days, the script can automatically create:
```
/opt/pcaps/
├── day1/
│   └── capture_day1.pcap
├── day2/
│   └── capture_day2.pcap
...
├── archiver.sh
└── archiver_error_log.txt
```

---

## 🛡️ License

This project is licensed under the [MIT License](./LICENSE).

---
