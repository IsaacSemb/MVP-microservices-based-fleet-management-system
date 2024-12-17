

# Consumer Configuration Object
class ConsumerConfig:
    """A class to hold consumer details such as queues, callbacks, and exchanges"""

    def __init__(self, queue_name, exchange, exchange_type, callback, routing_key=""):
        self.queue_name = queue_name
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.callback = callback
        self.routing_key = routing_key