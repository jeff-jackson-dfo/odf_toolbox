from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class RecordHeader(BaseModel, BaseHeader):
    """
    A class to represent a Record Header in an ODF object.
    """
    def __init__(self, 
                 num_calibration: int = 0, 
                 num_swing: int = 0,
                 num_history: int = 0,
                 num_cycle: int = 0,
                 num_param: int = 0,
                 ):
        super().__init__()
        self.num_calibration = num_calibration
        self.num_swing = num_swing
        self.num_history = num_history
        self.num_cycle = num_cycle
        self.num_param = num_param

    def log_record_message(self, field: str, old_value: str, new_value: str) -> NoReturn:
        message = f"In Record Header field {field.upper()} was changed from {old_value} to {new_value}"
        super().log_message(message)

    @property
    def num_calibration(self) -> int:
        return self._num_calibration

    @num_calibration.setter
    def num_calibration(self, value: int) -> NoReturn:
        self._num_calibration = value

    @property
    def num_swing(self) -> int:
        return self._num_swing

    @num_swing.setter
    def num_swing(self, value: int) -> NoReturn:
        self._num_swing = value

    @property
    def num_history(self) -> int:
        return self._num_history

    @num_history.setter
    def num_history(self, value: int) -> NoReturn:
        self._num_history = value

    @property
    def num_cycle(self) -> int:
        return self._num_cycle

    @num_cycle.setter
    def num_cycle(self, value: int) -> NoReturn:
        self._num_cycle = value

    @property
    def num_param(self) -> int:
        return self._num_param

    @num_param.setter
    def num_param(self, value: int) -> NoReturn:
        self._num_param = value

    def populate_object(self, record_fields: list) -> NoReturn:
        for record_line in record_fields:
            tokens = record_line.split('=', maxsplit=1)
            record_dict = odfutils.list_to_dict(tokens)
            for key, value in record_dict.items():
                key = key.strip()
                value = int(value)
                match key:
                    case 'NUM_CALIBRATION':
                        self.num_calibration = value
                    case 'NUM_SWING':
                        self.num_swing = value
                    case 'NUM_HISTORY':
                        self.num_history = value
                    case 'NUM_CYCLE':
                        self.num_cycle = value
                    case 'NUM_PARAM':
                        self.num_param = value

    def print_object(self) -> str:
        record_header_output = "RECORD_HEADER\n"
        record_header_output += f"  NUM_CALIBRATION = {self.num_calibration}\n"
        record_header_output += f"  NUM_HISTORY = {self.num_history}\n"
        record_header_output += f"  NUM_SWING = {self.num_swing}\n"
        record_header_output += f"  NUM_PARAM = {self.num_param}\n"
        record_header_output += f"  NUM_CYCLE = {self.num_cycle}\n"
        return record_header_output

def main():
    record = RecordHeader()
    record_fields = ["NUM_CALIBRATION = 1",
                    "NUM_HISTORY = 3",
                    "NUM_SWING = 0",
                    "NUM_PARAM = 5",
                    "NUM_CYCLE = 1000"]
    record.populate_object(record_fields)
    print(record.print_object())
    record.log_record_message('num_param', record.num_param, 17)
    record.num_param = 17
    print(record.print_object())
    for log_entry in BaseHeader.shared_log_list:
        print(log_entry)

if __name__ == "__main__":
    main()
