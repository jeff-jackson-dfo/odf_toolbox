from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel
from icecream import ic

class HistoryHeader(BaseModel, BaseHeader):
    """ A class to represent a History Header in an ODF object. """
    def __init__(self, 
                 creation_date: str = None, 
                 processes: list = None):
        super().__init__()
        self.creation_date = creation_date if creation_date is not None else BaseHeader.SYTM_NULL_VALUE
        self.processes = processes if processes is not None else []

    def log_history_message(self, field: str, old_value: str, new_value: str) -> NoReturn:
        assert isinstance(field, str), "Input argument 'field' must be a string."
        assert isinstance(old_value, str), "Input argument 'old_value' must be a string."
        assert isinstance(new_value, str), "Input argument 'new_value' must be a string."
        message = f'In History Header field {field.upper()} was changed from "{old_value}" to "{new_value}"'
        super().log_message(message)
        
    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("' ")
        self._creation_date = value.upper()

    @property
    def processes(self):
        return self._processes

    @processes.setter
    def processes(self, plist: list) -> NoReturn:
        assert isinstance(plist, list), "Input argument 'plist' must be a list."
        for p in plist:
            assert isinstance(p, str), "Input argument 'plist' must be a list of strings."
        self._processes = plist

    def set_process(self, process: str, process_number: int = 0) -> NoReturn:
        assert isinstance(process, str), "Input argument 'process' must be a string."
        assert isinstance(process_number, int), "Input argument 'process_number' must be a integer."
        assert process_number >= 0, "Input argument 'process_number' must be >= 0."
        process = process.strip("' ")
        number_of_processes = len(self.processes)
        if process_number == 0:
            self._processes.append(process)
        elif process_number <= number_of_processes and number_of_processes > 0:
            self._processes[process_number - 1] = process

    def add_process(self, process: str) -> NoReturn:
        assert isinstance(process, str), "Input argument 'process' must be a string."
        process = process.strip("' ")
        self._processes.append(process)

    def find_process(self, search_string: str) -> int:
        found_strings = []
        for i, process in enumerate(self.processes):
            if search_string in process:
                found_strings.append(i + 1)
        return found_strings

    def populate_object(self, history_fields: list) -> NoReturn:
        assert isinstance(history_fields, list), "Input argument 'history_fields' must be a list."      
        for header_line in history_fields:
            tokens = header_line.split('=', maxsplit=1)
            history_dict = odfutils.list_to_dict(tokens)
            for key, value in history_dict.items():
                key = key.strip()
                value = value.strip("' ")
                match key:
                    case 'CREATION_DATE':
                        self._creation_date = value
                    case 'PROCESS':
                        self.add_process(value)

    def print_object(self) -> str:
        history_header_output = "HISTORY_HEADER\n"
        history_header_output += f"  CREATION_DATE = '{self.creation_date}'\n"
        if self.processes:
            for process in self.processes:
                history_header_output += f"  PROCESS = '{process}'\n"
        else:
            history_header_output += "  PROCESS = ''\n"
        return history_header_output


def main():
    print()

    history = HistoryHeader()
    print(history.print_object())
    history_fields = ["CREATION_DATE = '01-jun-2021 00:00:00.00'",
                    "PROCESS = First process",
                    "PROCESS = Second process",
                    "PROCESS = Blank process",
                    "PROCESS = Fourth process",
                    "PROCESS = Last process"]
    history.populate_object(history_fields)
    print(history.print_object())
    history.log_history_message('process', history.processes[1], 'Bad Cast')
    history.set_process('Bad Cast', 2)
    print(history.print_object())
    ic(history.find_process('Bad Cast'))
    ic(history.find_process('Blank'))
    ic(history.find_process('process'))
    
    for log_entry in BaseHeader.shared_log_list:
        print(log_entry)
    print()

if __name__ == '__main__':
    main()