import os
import distutils.util

SLEEP_SECONDS = int(os.getenv('SLEEP_SECONDS'))
YIELD_TIME_SECONDS = int(os.getenv('YIELD_TIME_SECONDS'))
RANGE = int(os.getenv('RANGE'))
INDEX_FILE = os.getenv('INDEX_FILE')
