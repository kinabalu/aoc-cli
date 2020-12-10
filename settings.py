DEBUG = False

SESSION_KEY = None

AOC_URL = "https://adventofcode.com"
AOC_DOMAIN = ".adventofcode.com"
AOC_TIMEZONE = "US/Eastern"
AOC_RELEASE_HOUR=0
AOC_RELEASE_MINUTE=0
AOC_START_YEAR=2015

TIMEZONE = 'US/Pacific'

DATA_PATH = "./data/{year}"
DAY_FILE_FORMAT = "{day}.txt"

CODE_TEMPLATE_FILE = "code.py.template"
CODE_FILENAME_FORMAT = "{day}.py"

try:
    from local_settings import *
except ImportError:
    pass
