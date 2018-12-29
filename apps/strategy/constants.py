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
    "PORT": "7000",  # TODO: hardcoded
    "LOG_TRANSPORTS": "1",  # Transfer logs to file
    "LOG_PATH": os.path.join(settings.BASE_DIR, 'bots-logs'),  # Log file path
}
