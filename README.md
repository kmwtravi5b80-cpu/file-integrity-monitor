# Project 2: File Integrity Monitor

## Overview
A Python defensive security utility that creates a SHA-256 baseline of files in a directory and later detects added, modified, or deleted files.

## Skills demonstrated
- Cryptographic hashing (SHA-256)
- Python file and JSON handling
- File integrity monitoring concepts
- Change detection and basic security auditing

## Requirements
- Python 3.9 or newer
- No third-party packages

## Run the demonstration
Open a terminal in this project folder.

### 1. Create a baseline
```bash
python integrity_monitor.py baseline demo_files
```

### 2. Check for changes
```bash
python integrity_monitor.py check demo_files
```
This should report no changes.

### 3. Simulate an authorized lab change
Edit `demo_files/important.txt`, add a line, save it, and run:
```bash
python integrity_monitor.py check demo_files
```
The file should be reported as `[MODIFIED]`.

### 4. Restore the original sample (optional)
Restore the original contents shown in the file, then run the baseline command again.

## Safe use and limitations
Only monitor folders you own or are authorized to assess. A hash match shows file contents have not changed relative to the saved baseline; it does not prove a file is safe. Store the baseline separately with restricted write access. This demo does not run as a background service.
