# I've Been Misled - Toboggan

A CSE 5914 Knowledge Systems Capstone Project

[![Build Status](https://travis-ci.org/Ive-Been-Misled/Toboggan.svg?branch=master)](https://travis-ci.org/Ive-Been-Misled/Toboggan)

## Requirements

- Python 3.7 or later
- IBM Cloud account (free)

## How to Run

Broad instructions in the comments followed by example commands, which may vary
depending on your system

### Linux
```sh
# clone the repository
git clone https://github.com/Ive-Been-Misled/Toboggan.git
cd Toboggan

# setup and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip install .
spacy download en_core_web_sm

# set api key environment variable
export API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# launch a local web server and open the browser window
python3 -m toboggan.server
```
### Windows
```sh
# clone the repository
git clone https://github.com/Ive-Been-Misled/Toboggan.git
cd Toboggan

# setup and activate a Python virtual environment
python -m venv venv
. venv/Scripts/activate  # Be sure to include the '.'

# install pytorch as this must be installed manually on windows
pip3 install torch==1.3.0+cpu torchvision==0.4.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

# install dependencies
pip install poetry
poetry install
spacy download en_core_web_sm

# set api key environment variable
$env:API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# launch a local web server and open the browser window
python -m toboggan.server
```

Note: Exporting the `API_KEY` environment variable is only needed for the first
run. Subsequent runs will use the API key and workspace ID saved in
`toboggan/watson_api.json` (ignored by Git). When making changes to
`actions.json`, delete `toboggan/watson_api.json` in order to generate a new
workspace with the updated intents. When a new workspace is generated, it may
take a while to train -- calls to `ActionMapper#map` will return `None` for all
input until the training is complete.

### Fake GPT2 for testing
Due to the fact that GPT2 takes a very long time to create descriptions on machines that don't have Nvidia graphics cards, we created a fake GPT2 tokenizer that returns descriptions made up of random words. Obviously this does not function in the same way as GPT2, but it works great for testing.
#### To Enable run the following command:
Windows:
```$env:FAKE_GPT2='true'```

Linux:
```export FAKE_GPT2='true'```

#### And to Disable, run:
Windows:
```Remove-Item Env:\FAKE_GPT2```

Linux:
```unset FAKE_GPT2```

## Team Members
- JS Teoh
- Tom Paoloni
- Jonathan Karkour
- Em Zhan
