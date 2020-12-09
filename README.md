# AoC CLI

Here's a quick idea of code that can wait for the next day, and download
the data files along with creating a templated piece of code.

## Setup
Create a `local_settings.py` and include your session key, and timezone

The session key can be found in a cookie called "session" which should
be available after logging in to the adventofcode.com website. The timezone
should have a value such as `US/Pacific` or similar.

The rest are defaults and should be quite sensible. The `code.py.template`
can be changed to whatever you like. It is a jinja2 template and can be
modified to suit more parameters as needed.

Create a python virtual environment and install dependencies with something like 

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Commands
The following commands are available

* **wait** - `./app.py wait` will given the current time wait until the next
contest starts. It will pause once a second to update the current time and
once the time is ready, download the input data, and create the code file
for the given day based on `CODE_FILENAME_FORMAT`
* **download** - `./app.py download {day}` will download the input data and
optionally create the code file for the given day but won't overwrite unless
the argument `overwrite_existing` is passed in as true (default is false)
* **view** - `./app.py download {day}` will download and allow to you to view
the html for the given day. Future is to parse this out to create a markdown
file to make it easier to read