from odf_toolbox.basehdr import BaseHeader
from odf_toolbox import odfutils

class CruiseHeader(BaseHeader):
    
    def __init__(self):
        super().__init__()
        self._country_institute_code = None
        self._cruise_number = ''
        self._organization = ''
        self._chief_scientist = ''
        self._start_date = ''
        self._end_date = ''
        self._platform = ''
        self._area_of_operation = ''
        self._cruise_name = ''
        self._cruise_description = ''

    def log_message(self, message):
        super().log_message(f'CRUISE_HEADER: {message}')

    def get_country_institute_code(self) -> int:
        return self._country_institute_code

    def set_country_institute_code(self, value: int, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to int
            try:
                value = int(value)
            except ValueError:
                f"Input value could not be successfully converted to type int: {value}"
        assert isinstance(value, int), \
               f"Input value is not of type int: {value}"
        if not read_operation:
            self.log_message(f'COUNTRY_INSTITUTE_CODE was changed from {self._country_institute_code} '
                                 f'to {value}')
        self._country_institute_code = value

    def get_cruise_number(self) -> str:
        return self._cruise_number

    def set_cruise_number(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'CRUISE_NUMBER was changed from "{self._cruise_number}" to "{value}"')
        self._cruise_number = f"{value}"

    def get_organization(self) -> str:
        return self._organization

    def set_organization(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'ORGANIZATION was changed from "{self._organization}" to "{value}"')
        self._organization = f"{value.strip()}"

    def get_chief_scientist(self) -> str:
        return self._chief_scientist

    def set_chief_scientist(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'CHIEF_SCIENTIST was changed from "{self._chief_scientist}" to "{value}"')
        self._chief_scientist = f'{value}'

    def get_start_date(self) -> str:
        return self._start_date

    def set_start_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'START_DATE was changed from "{self._start_date}" to "{value}"')
        self._start_date = f'{value}'

    def get_end_date(self) -> str:
        return self._end_date

    def set_end_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'END_DATE was changed from "{self._end_date}" to "{value}"')
        self._end_date = f'{value}'

    def get_platform(self) -> str:
        return self._platform

    def set_platform(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'PLATFORM was changed from "{self._platform}" to "{value}"')
        self._platform = f'{value}'

    def get_area_of_operation(self) -> str:
        return self._area_of_operation

    def set_area_of_operation(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'AREA_OF_OPERATION was changed from "{self._area_of_operation}" to "{value}"')
        self._area_of_operation = f'{value}'

    def get_cruise_name(self) -> str:
        return self._cruise_name

    def set_cruise_name(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'CRUISE_NAME was changed from "{self._cruise_name}" to "{value}"')
        self._cruise_name = f'{value}'

    def get_cruise_description(self) -> str:
        return self._cruise_description

    def set_cruise_description(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'CRUISE_DESCRIPTION was changed from "{self._cruise_description}" to "{value}"')
        self._cruise_description = f'{value}'

    def populate_object(self, cruise_fields: list):
        assert isinstance(cruise_fields, list), \
               f"Input value is not of type list: {cruise_fields}"
        for header_line in cruise_fields:
            tokens = header_line.split('=', maxsplit=1)
            cruise_dict = odfutils.list_to_dict(tokens)
            for key, value in cruise_dict.items():
                key = key.strip()
                value = value.strip()
                match key:
                    case 'COUNTRY_INSTITUTE_CODE':
                        self.set_country_institute_code(value, read_operation=True)
                    case 'CRUISE_NUMBER':
                        self.set_cruise_number(value, read_operation=True)
                    case 'ORGANIZATION':
                        self.set_organization(value, read_operation=True)
                    case 'CHIEF_SCIENTIST':
                        self.set_chief_scientist(value, read_operation=True)
                    case 'START_DATE':
                        self.set_start_date(value, read_operation=True)
                    case 'END_DATE':
                        self.set_end_date(value, read_operation=True)
                    case 'PLATFORM':
                        self.set_platform(value, read_operation=True)
                    case 'AREA_OF_OPERATION':
                        self.set_area_of_operation(value, read_operation=True)
                    case 'CRUISE_NAME':
                        self.set_cruise_name(value, read_operation=True)
                    case 'CRUISE_DESCRIPTION':
                        self.set_cruise_description(value, read_operation=True)
        return self

    def print_object(self, file_version: int = 2) -> str:
        assert isinstance(file_version, int), \
               f"Input file_version is not of type int: {file_version}"
        cruise_header_output = "CRUISE_HEADER\n"
        cruise_header_output += (f"  COUNTRY_INSTITUTE_CODE = "
                                 f"{odfutils.check_int(self.get_country_institute_code())}\n")
        cruise_header_output += f"  CRUISE_NUMBER = '{self.get_cruise_number()}'\n"
        cruise_header_output += f"  ORGANIZATION = '{self.get_organization()}'\n"
        cruise_header_output += f"  CHIEF_SCIENTIST = '{self.get_chief_scientist()}'\n"
        cruise_header_output += f"  START_DATE = '{odfutils.check_datetime(self.get_start_date())}'\n"
        cruise_header_output += f"  END_DATE = '{odfutils.check_datetime(self.get_end_date())}'\n"
        cruise_header_output += f"  PLATFORM = '{self.get_platform()}'\n"
        if file_version == 3:
            cruise_header_output += f"  AREA_OF_OPERATION = '{self.get_area_of_operation()}'\n"
        cruise_header_output += f"  CRUISE_NAME = '{self.get_cruise_name()}'\n"
        cruise_header_output += f"  CRUISE_DESCRIPTION = '{self.get_cruise_description()}'\n"
        return cruise_header_output


if __name__ == "__main__":

    cruise = CruiseHeader()
    cruise.set_chief_scientist('Jeff Jackson')
    cruise.set_organization("DFO BIO")
    print(cruise.print_object())
