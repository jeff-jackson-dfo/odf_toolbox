from odf_toolbox.basehdr import BaseHeader
from odf_toolbox import odfutils

class RecordHeader(BaseHeader):

    def __init__(self):
        super().__init__()
        self._num_calibration = 0
        self._num_swing = 0
        self._num_history = 0
        self._num_cycle = 0
        self._num_param = 0

    def log_message(self, message):
        super().log_message(f"RECORD_HEADER: {message}")

    def get_num_calibration(self) -> int:
        return self._num_calibration

    def set_num_calibration(self, value: int, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to int
            try:
                value = int(value)
            except ValueError:
                f"Input value could not be successfully converted to type int: {value}"
        assert isinstance(value, int), \
               f"Input value is not of type int: {value}"
        if not read_operation:
            self.log_message(f"NUM_CALIBRATION was changed from {self._num_calibration} to {value}")
        self._num_calibration = value

    def get_num_swing(self) -> int:
        return self._num_swing

    def set_num_swing(self, value: int, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to int
            try:
                value = int(value)
            except ValueError:
                f"Input value could not be successfully converted to type int: {value}"
        assert isinstance(value, int), \
               f"Input value is not of type int: {value}"
        if not read_operation:
            self.log_message(f"NUM_SWING was changed from {self._num_swing} to {value}")
        self._num_swing = value

    def get_num_history(self) -> int:
        return self._num_history

    def set_num_history(self, value: int, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to int
            try:
                value = int(value)
            except ValueError:
                f"Input value could not be successfully converted to type int: {value}"
        assert isinstance(value, int), \
               f"Input value is not of type int: {value}"
        if not read_operation:
            self.log_message(f"NUM_HISTORY was changed from {self._num_history} to {value}")
        self._num_history = value

    def get_num_cycle(self) -> int:
        return self._num_cycle

    def set_num_cycle(self, value: int, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to int
            try:
                value = int(value)
            except ValueError:
                f"Input value could not be successfully converted to type int: {value}"
        assert isinstance(value, int), \
               f"Input value is not of type int: {value}"
        if not read_operation:
            self.log_message(f"NUM_CYCLE was changed from {self._num_cycle} to {value}")
        self._num_cycle = value

    def get_num_param(self) -> int:
        return self._num_param

    def set_num_param(self, value: int, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to int
            try:
                value = int(value)
            except ValueError:
                f"Input value could not be successfully converted to type int: {value}"
        assert isinstance(value, int), \
               f"Input value is not of type int: {value}"
        if not read_operation:
            self.log_message(f"NUM_PARAM was changed from {self._num_param} to {value}")
        self._num_param = value

    def populate_object(self, record_fields: list) -> None:
        assert isinstance(record_fields, list), \
               f"Input value is not of type list: {record_fields}"
        for record_line in record_fields:
            tokens = record_line.split('=', maxsplit=1)
            record_dict = odfutils.list_to_dict(tokens)
            for key, value in record_dict.items():
                key = key.strip()
                value = value.strip()
                match key:
                    case 'NUM_CALIBRATION':
                        self.set_num_calibration(value, read_operation=True)
                    case 'NUM_SWING':
                        self.set_num_swing(value, read_operation=True)
                    case 'NUM_HISTORY':
                        self.set_num_history(value, read_operation=True)
                    case 'NUM_CYCLE':
                        self.set_num_cycle(value, read_operation=True)
                    case 'NUM_PARAM':
                        self.set_num_param(value, read_operation=True)

    def print_object(self) -> str:
        record_header_output = "RECORD_HEADER\n"
        record_header_output += f"  NUM_CALIBRATION = {odfutils.check_int_value(self.get_num_calibration())}\n"
        record_header_output += f"  NUM_HISTORY = {odfutils.check_int_value(self.get_num_history())}\n"
        record_header_output += f"  NUM_SWING = {odfutils.check_int_value(self.get_num_swing())}\n"
        record_header_output += f"  NUM_PARAM = {odfutils.check_int_value(self.get_num_param())}\n"
        record_header_output += f"  NUM_CYCLE = {odfutils.check_int_value(self.get_num_cycle())}\n"
        return record_header_output
