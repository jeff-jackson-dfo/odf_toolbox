from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class HistoryHeader(BaseModel, BaseHeader):
    """
    A class to represent a History Header in an ODF object.
    """        
    def __init__(self, 
                 creation_date: str = BaseHeader.sytm_null_value, 
                 processes: list = None):
        super().__init__()
        self.creation_date = creation_date
        self.processes = processes if processes is not None else []

    def log_history_message(self, field: str, old_value: str, new_value: str) -> NoReturn:
        message = f'In History Header field {field.upper()} was changed from "{old_value}" to "{new_value}"'
        super().log_message(message)
        
    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, value: str) -> NoReturn:
        value = value.strip("' ")
        self._creation_date = value.upper()

    @property
    def processes(self):
        return self._processes

    @processes.setter
    def processes(self, plist: list) -> NoReturn:
        self._processes = plist

    def set_process(self, process: str, process_number: int = 0) -> NoReturn:
        process = process.strip("' ")
        number_of_processes = len(self.processes)
        if process_number == 0 and number_of_processes >= 0:
            self._processes.append(process)
        elif process_number <= number_of_processes and number_of_processes > 0:
            self._processes[process_number-1] = process
        else:
            raise ValueError("The 'process' number does not match the number of PROCESS lines.")

    def add_process(self, process: str) -> NoReturn:
        process = process.strip("' ")
        self._processes.append(process)

    def populate_object(self, history_fields: list) -> NoReturn:
        for header_line in history_fields:
            tokens = header_line.split('=', maxsplit=1)
            history_dict = odfutils.list_to_dict(tokens)
            for key, value in history_dict.items():
                key = key.strip()
                value = value.strip("' ")
                match key:
                    case 'CREATION_DATE':
                        self.creation_date = value
                    case 'PROCESS':
                        self.add_process(value)

    def print_object(self) -> str:
        history_header_output = "HISTORY_HEADER\n"
        history_header_output += f"  CREATION_DATE = '{odfutils.check_datetime(self.creation_date)}'\n"
        if self.processes:
            for process in self.processes:
                history_header_output += f"  PROCESS = '{process}'\n"
        else:
            history_header_output += "  PROCESS = ''\n"
        return history_header_output


def main():
    history = HistoryHeader()
    print(history.print_object())
    history_fields = ["CREATION_DATE = '01-jun-2021 00:00:00.00'",
                    "PROCESS = First process",
                    "PROCESS = Last process"]
    history.populate_object(history_fields)
    print(history.print_object())
    history.log_history_message('process', history.processes[1], 'Bad Cast')
    history.set_process('Bad Cast', 2)
    print(history.print_object())

    for log_entry in BaseHeader.shared_log_list:
        print(log_entry)


if __name__ == '__main__':
    main()