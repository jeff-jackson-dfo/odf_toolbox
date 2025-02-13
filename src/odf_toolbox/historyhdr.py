from odf_toolbox import odfutils

class HistoryHeader:
    def __init__(self):
        self._creation_date = "''"
        self._processes = []

    def get_creation_date(self):
        return self._creation_date

    def set_creation_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            odfutils.logger.info(f"History_Header.Creation_Date changed from {self._creation_date} to '{value}'")
        self._creation_date = f"'{value}'"

    def get_process(self):
        return self._processes

    def set_process(self, process: str, process_number: int = 0, read_operation: bool = False) -> None:
        assert isinstance(process, str), \
               f"Input value is not of type str: {process}"
        assert isinstance(process_number, int), \
               f"Input value is not of type int: {process_number}"
        process = process.strip("\' ")
        number_of_processes = len(self._processes)
        if process_number == 0 and number_of_processes >= 0:
            if not read_operation:
                odfutils.logger.info(f"The following Process line was added to the History_Header: '{process}'")
            self._processes.append(f"'{process}'")
        elif process_number <= number_of_processes and number_of_processes > 0:
            odfutils.logger.info(f"Process {process_number} in History_Header.Processes was changed from "
                                 f"{self._processes[process_number - 1]} to '{process}'")
            self._processes[process_number-1] = f"'{process}'"
        else:
            raise ValueError("The Process number does not match the number of Process lines.")

    def add_process(self, process: str) -> None:
        assert isinstance(process, str), \
               f"Input value is not of type str: {process}"
        process = process.strip("\'")
        self._processes.append(f"'{process}'")

    def populate_object(self, history_fields: list):
        assert isinstance(history_fields, list), \
               f"Input value is not of type list: {history_fields}"
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
        history_header_output += f"  CREATION_DATE = {odfutils.check_datetime(self.get_creation_date())}\n"
        if self.get_process():
            for process in self.get_process():
                history_header_output += f"  PROCESS = {process}\n"
        else:
            history_header_output += "  PROCESS = ''\n"
        return history_header_output
