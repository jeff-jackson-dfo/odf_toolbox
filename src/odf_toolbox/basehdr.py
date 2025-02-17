import logging

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
        self.configure_logging()
    
    def configure_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)

    def reset_logging(self):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        self.configure_logging()

    @classmethod
    def reset_log_list(cls):
        cls.shared_log_list = []

    def log_message(self, message):
        # self.logger.info(message)
        self.shared_log_list.append(message)


if __name__ == "__main__":

    class SubClassA(BaseHeader):
        def log_message(self, message):
            super().log_message(f"SubClassA: {message}")

    class SubClassB(BaseHeader):
        def log_message(self, message):
            super().log_message(f"SubClassB: {message}")

    # Example usage
    subclass_a = SubClassA()
    subclass_b = SubClassB()

    subclass_a.log_message("Message from SubClassA")
    subclass_b.log_message("Message from SubClassB")

    # Access the shared log messages before resetting
    print("Shared log messages before resetting:")
    for log_entry in BaseHeader.shared_log_list:
        print(log_entry)

    # Reset the shared log list
    BaseHeader.reset_log_list()

    # Access the shared log messages after resetting
    print("Shared log messages after resetting:")
    print(BaseHeader.shared_log_list)

    subclass_a.log_message("New message from SubClassA after reset")
    subclass_b.log_message("New message from SubClassB after reset")

    # Access the shared log messages after new log entries
    print("Shared log messages after new entries:")
    for log_entry in BaseHeader.shared_log_list:
        print(log_entry)

