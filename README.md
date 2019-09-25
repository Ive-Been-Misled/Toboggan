# I've Been Misled - Toboggan

A CSE 5914 Knowledge Systems Capstone Project

[![Build Status](https://travis-ci.org/Ive-Been-Misled/Toboggan.svg?branch=master)](https://travis-ci.org/Ive-Been-Misled/Toboggan)

## Requirements

- Python 3.7 or later
- IBM Cloud account (free)

## How to Run

Broad instructions in the comments followed by example commands, which may vary
depending on your system

```sh
# clone the repository
git clone https://github.com/Ive-Been-Misled/Toboggan.git
cd Toboggan

# setup and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate  # `source venv/Scripts/activate` on Windows

# install dependencies
pip install .

# set api key environment variable
export API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# launch a local web server and open the browser window
python3 -m toboggan.server
```

## Team Members
- JS Teoh
- Tom Paoloni
- Jonathan Karkour
- Em Zhan
