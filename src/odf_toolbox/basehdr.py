import logging
from typing import ClassVar
from pydantic import BaseModel, Field

# Logger class that inherits from Pydantic's BaseModel
class LoggerConfig(BaseModel):
    # Define the logging level as a field with a default value
    log_level: str = Field(default='INFO', description='Logging level (e.g., DEBUG, INFO, WARNING, ERROR)')

    def configure_logger(self):
        """Configure the logger based on the settings in the model."""
        logger = logging.getLogger()
        level = getattr(logging, self.log_level.upper(), logging.INFO)
        logger.setLevel(level)

        # Clear any existing handlers
        for handler in logger.root.handlers:
            logger.root.removeHandler(handler)

        return logger


# Main Logger class using the LoggerConfig for configuration
class BaseHeader:
    """
    This Base Header class is used to create the logging functionality to be 
    utilized by the subclasses.
    """
    # Shared log list to store the log entries for all instances of the class
    shared_log_list: ClassVar[list] = []

    # Various null values
    null_value: ClassVar[float] = -999.0
    sytm_null_value: ClassVar[str] = '17-NOV-1858 00:00:00.00'

    def __init__(self, config: LoggerConfig):
        self.config = config
        self.logger = self.config.configure_logger()

    def log(self, message: str, level: str = 'INFO'):
        """Log a message with the specified level."""
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message)

# Usage example    
    def reset_logging(self):
        self.logger = self.config.configure_logger()

    @classmethod
    def reset_log_list(cls):
        cls.shared_log_list = []

    def log_message(self, message):
        # self.logger.info(message)
        self.shared_log_list.append(message)

def main():

    # Create a config object using Pydantic
    config = LoggerConfig(log_level = "INFO")

    class SubClassA(BaseHeader):
        def log_message(self, message):
            super().log_message(f"SubClassA: {message}")

    class SubClassB(BaseHeader):
        def log_message(self, message):
            super().log_message(f"SubClassB: {message}")

    # Example usage
    subclass_a = SubClassA(config)
    subclass_b = SubClassB(config)

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


if __name__ == "__main__":

    main()