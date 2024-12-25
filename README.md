# Normalize Audio with Python + SoX

This repository provides a simple Python script to **normalize audio files** using [SoX (Sound eXchange)](http://sox.sourceforge.net/). The script uses a Windows file dialog to select audio files and saves the normalized files **in the same folder**, appending `_normalized` to the filename.

---

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
   - [Install Python 3](#install-python-3)
   - [Install SoX](#install-sox)
   - [Add SoX to Windows PATH](#add-sox-to-windows-path)
4. [Usage](#usage)
5. [Script: `normalize_in_place.py`](#script-normalize_in_placepy)
6. [License](#license)
7. [Credits](#credits)

---

## Features

- **Windows Explorer file dialog** for easy file selection.
- **Batch processing** of multiple audio files in one go.
- **Normalization** to the maximum possible level without clipping (`gain -n`).
- **In-place** creation of normalized files with `_normalized` in the filename.

---

## Prerequisites

- **Windows** (although SoX and Python are cross-platform, this example specifically uses Windows dialogs).
- **Python 3.x** (with `tkinter` installed—this is usually included by default on Windows).
- **SoX** installed and added to your system’s PATH.

---

## Installation

### Install Python 3

1. Go to [Python Downloads](https://www.python.org/downloads/).
2. Download and run the **Windows** installer.
3. During installation, **check** “Add Python to PATH” or manually add it later.

### Install SoX

1. Download **SoX** from the official [SoX website](http://sox.sourceforge.net/)
2. Unzip or install to a folder, for example: C:\Program Files\sox


### Add SoX to Windows PATH

1. Press **Windows key**, type “Edit the system environment variables,” and open it.
2. In the **System Properties** dialog, go to the **Advanced** tab, then click **Environment Variables**.
3. Under **System variables**, find **Path**, select it, and click **Edit**.
4. Click **New**, then **Browse** to the folder where you installed SoX (e.g., `C:\Program Files\sox`).
5. Click **OK** to confirm.

To check if SoX is now in your PATH, open **Command Prompt** or **PowerShell** and run: sox --version


### Usage
- python normalize_in_place.py \n or
- run bat file
