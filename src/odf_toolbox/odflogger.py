# -*- coding: utf-8 -*-
import logging
from odf_toolbox.listhandler import ListHandler


class ODFLogger:
    """
    ODF Logger Class

    This class is responsible for recording all modifications done to an OdfHeader object.

    """

    def __init__(self):
        """
        Method that initializes an ODFLogger class object.
        """
        self.logger = logging.getLogger("ODFLogger")

        # Configure logging for the custom handler
        list_handler = ListHandler()
        self.logger.addHandler(list_handler)
        self.logger.setLevel(logging.INFO)  # Set the logging level as needed

