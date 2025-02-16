import logging


# Define a custom handler that logs modifications done to subclass headers
class ListHandler(logging.Handler):

    def __init__(self, shared_log_list):
        super().__init__()
        self.log_list = shared_log_list

    def emit(self, record):
        log_entry = self.format(record)
        self.log_list.append(log_entry)


class BaseHeader:
    """
    Base Header Class

    This base class is creates the logging functionality to be utilized by the subclasses.

    """

    # Shared log list to store the log entries for all instances of the class
    shared_log_list = []

    def __init__(self):
        """
        Method that initializes a base class object.
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        # Configure logging for the custom handler
        if not self.logger.hasHandlers():
            self.list_handler = ListHandler(BaseHeader.shared_log_list)
            self.logger.addHandler(self.list_handler)
            self.logger.setLevel(logging.INFO)  # Set the logging level as needed
