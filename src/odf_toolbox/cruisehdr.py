from odf_toolbox.basehdr import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class CruiseHeader(BaseModel, BaseHeader):
    """ A class to represent a Cruise Header in an ODF object. """
    def __init__(self, 
                 country_institute_code: int = None, 
                 cruise_number: str = None, 
                 organization: str = None, 
                 chief_scientist: str = None, 
                 start_date: str = None, 
                 end_date: str = None, 
                 platform: str = None,
                 area_of_operation: str = None, 
                 cruise_name: str = None, 
                 cruise_description: str = None
                 ) -> NoReturn:
        super().__init__()
        self.country_institute_code = country_institute_code if country_institute_code is not None else 0
        self.cruise_number = cruise_number if cruise_number is not None else ''
        self.organization = organization if organization is not None else ''
        self.chief_scientist = chief_scientist if chief_scientist is not None else ''
        self.start_date = start_date if start_date is not None else BaseHeader.SYTM_NULL_VALUE
        self.end_date = end_date if end_date is not None else BaseHeader.SYTM_NULL_VALUE
        self.platform = platform if platform is not None else ''
        self.area_of_operation = area_of_operation if area_of_operation is not None else ''
        self.cruise_name = cruise_name if cruise_name is not None else ''
        self.cruise_description = cruise_description if cruise_description is not None else ''

    def log_cruise_message(self, field: str, old_value: any, new_value: any) -> NoReturn:
        assert isinstance(field, str), "Input argument 'field' must be a string."
        if field.upper() == 'COUNTRY_INSTITUTE_CODE':
            message = f"In Cruise Header field {field.upper()} was changed from {old_value} to {new_value}"
        else:
            message = f'In Cruise Header field {field.upper()} was changed from "{old_value}" to "{new_value}"'
        super().log_message(message)

    @property
    def country_institute_code(self) -> int:
        return self._country_institute_code

    @country_institute_code.setter
    def country_institute_code(self, value: int) -> NoReturn:
        assert isinstance(value, int), "Input argument 'value' must be an integer."
        self._country_institute_code = value

    @property
    def cruise_number(self) -> str:
        return self._cruise_number

    @cruise_number.setter
    def cruise_number(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be an string."
        value = value.strip("\' ")
        self._cruise_number = value

    @property
    def organization(self) -> str:
        return self._organization

    @organization.setter
    def organization(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be an string."
        value = value.strip("\' ")
        self._organization = value

    @property
    def chief_scientist(self) -> str:
        return self._chief_scientist

    @chief_scientist.setter
    def chief_scientist(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be an string."
        value = value.strip("\' ")
        self._chief_scientist = value

    @property
    def start_date(self) -> str:
        return self._start_date

    @start_date.setter
    def start_date(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be an string."
        value = value.strip("\' ")
        self._start_date = value

    @property
    def end_date(self) -> str:
        return self._end_date

    @end_date.setter
    def end_date(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be an string."
        value = value.strip("\' ")
        self._end_date = value

    @property
    def platform(self) -> str:
        return self._platform

    @platform.setter
    def platform(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be an string."
        value = value.strip("\' ")
        self._platform = value

    @property
    def area_of_operation(self) -> str:
        return self._area_of_operation

    @area_of_operation.setter
    def area_of_operation(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be an string."
        value = value.strip("\' ")
        self._area_of_operation = value

    @property
    def cruise_name(self) -> str:
        return self._cruise_name

    @cruise_name.setter
    def cruise_name(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be an string."
        value = value.strip("\' ")
        self._cruise_name = value

    @property
    def cruise_description(self) -> str:
        return self._cruise_description

    @cruise_description.setter
    def cruise_description(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be an string."
        value = value.strip("\' ")
        self._cruise_description = value

    def populate_object(self, cruise_fields: list):
        # assert isinstance(cruise_fields, list), "Input argument 'cruise_fields' must be a list."
        for header_line in cruise_fields:
            tokens = header_line.split('=', maxsplit=1)
            cruise_dict = odfutils.list_to_dict(tokens)
            for key, value in cruise_dict.items():
                key = key.strip()
                value = value.strip()
                match key:
                    case 'COUNTRY_INSTITUTE_CODE':
                        self.country_institute_code = int(value)
                    case 'CRUISE_NUMBER':
                        self.cruise_number = value
                    case 'ORGANIZATION':
                        self.organization = value
                    case 'CHIEF_SCIENTIST':
                        self.chief_scientist = value
                    case 'START_DATE':
                        self.start_date = value
                    case 'END_DATE':
                        self.end_date = value
                    case 'PLATFORM':
                        self.platform = value
                    case 'AREA_OF_OPERATION':
                        self.area_of_operation = value
                    case 'CRUISE_NAME':
                        self.cruise_name = value
                    case 'CRUISE_DESCRIPTION':
                        self.cruise_description = value
        return self

    def print_object(self, file_version: float = 2.0) -> str:
        assert isinstance(file_version, float), "Input argument 'file_version' must be a float."
        cruise_header_output = "CRUISE_HEADER\n"
        cruise_header_output += f"  COUNTRY_INSTITUTE_CODE = {self.country_institute_code}\n"
        cruise_header_output += f"  CRUISE_NUMBER = '{self.cruise_number}'\n"
        cruise_header_output += f"  ORGANIZATION = '{self.organization}'\n"
        cruise_header_output += f"  CHIEF_SCIENTIST = '{self.chief_scientist}'\n"
        cruise_header_output += f"  START_DATE = '{self.start_date}'\n"
        cruise_header_output += f"  END_DATE = '{self.end_date}'\n"
        cruise_header_output += f"  PLATFORM = '{self.platform}'\n"
        if file_version == 3.0:
            cruise_header_output += f"  AREA_OF_OPERATION = '{self.area_of_operation}'\n"
        cruise_header_output += f"  CRUISE_NAME = '{self.cruise_name}'\n"
        cruise_header_output += f"  CRUISE_DESCRIPTION = '{self.cruise_description}'\n"
        return cruise_header_output


def main():
    print()
    cruise = CruiseHeader()
    print(cruise.print_object())
    cruise.log_cruise_message('COUNTRY_INSTITUTE_CODE', str(cruise.country_institute_code), 1805)
    cruise.country_institute_code = 1805
    cruise.log_cruise_message('CHIEF_SCIENTIST', cruise.chief_scientist, 'Jeff Jackson')
    cruise.chief_scientist = 'Jeff Jackson'
    cruise.log_cruise_message('organization', cruise.organization, "DFO BIO")
    cruise.organization = "DFO BIO"
    print(cruise.print_object())
    for log_entry in BaseHeader.shared_log_list:
        print(log_entry)
    print()


if __name__ == "__main__":
    main()
