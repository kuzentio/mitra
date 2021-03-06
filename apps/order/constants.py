from datetime import datetime

ORDER_TYPE_BUY = 'BUY'
ORDER_TYPE_SELL = 'SELL'

BITTREX = 'bittrex'
POLONIEX = 'poloniex'

EXCHANGES_CHOICES = [
    ('bittrex', 'Bittrex'),
    ('poloniex', 'Poloniex'),
]

ORDER_TYPE_CHOICES = [
    (ORDER_TYPE_BUY, 'Buy',),
    (ORDER_TYPE_SELL, 'Sell')
]

DEFAULT_MIN_DATE = datetime(2010, 1, 1)
DEFAULT_MAX_DATE = datetime(2020, 1, 1)

BITTREX_ORDER_MAPPING = (
    ('OrderUuid', 'uuid',),
    ('Exchange', 'pair'),
    ('Type', 'type'),
    ('OrderType', 'type'),
    ('Quantity', 'quantity'),
    ('Limit', 'price'),
    ('CommissionPaid', 'commission'),
    ('Commission', 'commission'),
    ('Price', '-'),
    ('Opened', 'opened_at'),
    ('TimeStamp', 'opened_at'),
    ('Closed', 'closed_at'),
)

POLONIEX_ORDER_MAPPING = (
    ('orderNumber', 'uuid',),
    ('type', 'type'),
    ('total', '-'),
    ('amount', 'quantity'),
    ('rate', '-'),
    ('date', '-'),
    ('globalTradeID', '-'),
    ('tradeID', '-'),
    ('fee', '-'),
    ('TimeStamp', 'opened_at'),
    ('category', '-'),
)
