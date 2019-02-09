import os
from collections import OrderedDict

from django.conf import settings

from config.settings.base import SECRET_KEY

CREATE_STRATEGY_DEFAULTS = OrderedDict([
    ("EXCHANGE", ""),
    ("KEY", ""),
    ("SECRET", ""),
    ("NAME_COIN", ""),
    ("NAME_COIN_TWO", ""),
])

STRATEGY_WEB_AUT_ENV = {
    "WEB_AUTH_KEY": SECRET_KEY,
    # "TIME_ZONE": "Europe/Kiev",  # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    "TIME_ZONE": "UTC",  # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    "LOG_TRANSPORTS": "1",  # Transfer logs to file
    # "LOG_DEBUG": "true",  #
    "LOG_PATH": os.path.join(settings.BASE_DIR, 'bots-logs'),  # Log file path
}
