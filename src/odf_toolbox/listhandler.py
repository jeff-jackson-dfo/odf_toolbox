import logging


# Define a custom handler that logs modifications done to an odfHeader instance in a list
class ListHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.log_records = []

    def emit(self, record):
        self.log_records.append(self.format(record))
