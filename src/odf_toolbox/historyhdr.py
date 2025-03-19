from odf_toolbox import BaseHeader
from odf_toolbox import odfutils

class HistoryHeader(BaseHeader):
    
    def __init__(self):
        super().__init__()
        self._creation_date = ''
        self._processes = []

    def log_message(self, message):
        # super().log_message(f"In History Header field {message}")
        super().log_message(message)
        
    def get_creation_date(self):
        return self._creation_date

    def set_creation_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'CREATION_DATE changed from "{self._creation_date}" to "{value}"')
        self._creation_date = f'{value}'

    def get_process(self):
        return self._processes

    def set_process(self, process: str, process_number: int = 0, read_operation: bool = False) -> None:
        assert isinstance(process, str), f"Input value is not of type str: {process}"
        assert isinstance(process_number, int), f"Input value is not of type int: {process_number}"
        process = process.strip("\' ")
        number_of_processes = len(self._processes)
        if process_number == 0 and number_of_processes >= 0:
            if not read_operation:
                self.log_message(f"The following PROCESS line was added to the History_Header: '{process}'")
            self._processes.append(f"{process}")
        elif process_number <= number_of_processes and number_of_processes > 0:
            self.log_message(f"PROCESS {process_number} was changed from "
                                 f"{self._processes[process_number - 1]} to '{process}'")
            self._processes[process_number-1] = f"{process}"
        else:
            raise ValueError("The 'process' number does not match the number of PROCESS lines.")

    def add_process(self, process: str) -> None:
        assert isinstance(process, str), "Input value is not of type str: {process}"
        process = process.strip("\'")
        self._processes.append(f"{process}")

    def populate_object(self, history_fields: list):
        assert isinstance(history_fields, list), f"Input value is not of type list: {history_fields}"
        for header_line in history_fields:
            tokens = header_line.split('=', maxsplit=1)
            history_dict = odfutils.list_to_dict(tokens)
            for key, value in history_dict.items():
                key = key.strip()
                value = value.strip()
                match key:
                    case 'CREATION_DATE':
                        self.set_creation_date(value, read_operation=True)
                    case 'PROCESS':
                        self.set_process(value, read_operation=True)

    def print_object(self) -> str:
        history_header_output = "HISTORY_HEADER\n"
        history_header_output += f"  CREATION_DATE = '{odfutils.check_datetime(self.get_creation_date())}'\n"
        if self.get_process():
            for process in self.get_process():
                history_header_output += f"  PROCESS = '{process}'\n"
        else:
            history_header_output += "  PROCESS = ''\n"
        return history_header_output


    def main():
        history = HistoryHeader()
        history_fields = ["CREATION_DATE = '2021-06-01 00:00:00'",
                        "PROCESS = First process",
                        "PROCESS = Last process"]
        history.populate_object(history_fields)
        print(history.print_object())

if __name__ == '__main__':
    
    HistoryHeader.main()