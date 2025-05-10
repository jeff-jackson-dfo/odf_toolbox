from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class InstrumentHeader(BaseModel, BaseHeader):
    """
    A class to represent an Instrument Header in an ODF object.
    """
    def __init__(self, 
                 instrument_type: str = '', 
                 model: str = '', 
                 serial_number: str = '', 
                 description: str = ''
                 ) -> NoReturn:
        super().__init__()
        self.instrument_type = instrument_type
        self.model = model
        self.serial_number = serial_number
        self.description = description

    def log_instrument_message(self, field: str, old_value: any, new_value: any) -> NoReturn:
        old_value = "''"
        message = f"In Instrument Header field {field.upper()} was changed from {old_value} to '{new_value}'"
        super().log_message(message)

    @property
    def instrument_type(self) -> str:
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, value: str) -> NoReturn:
        self._instrument_type = value

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str) -> NoReturn:
        self._model = value

    @property
    def serial_number(self) -> str:
        return self._serial_number

    @serial_number.setter
    def serial_number(self, value: str) -> NoReturn:
        self._serial_number = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> NoReturn:
        self._description = value

    def populate_object(self, instrument_fields: list):
        for header_line in instrument_fields:
            tokens = header_line.split('=', maxsplit=1)
            instrument_dict = odfutils.list_to_dict(tokens)
            for key, value in instrument_dict.items():
                key = key.strip()
                value = value.strip("' ")
                match key:
                    case 'INST_TYPE':
                        self.instrument_type = value
                    case 'MODEL':
                        self.model = value
                    case 'SERIAL_NUMBER':
                        self.serial_number = value
                    case 'DESCRIPTION':
                        self.description = value
        return self
    
    def print_object(self) -> str:
        instrument_header_output = "INSTRUMENT_HEADER\n"
        instrument_header_output += f"  INST_TYPE = '{odfutils.check_string(self.instrument_type)}'\n"
        instrument_header_output += f"  MODEL = '{odfutils.check_string(self.model)}'\n"
        instrument_header_output += f"  SERIAL_NUMBER = '{odfutils.check_string(self.serial_number)}'\n"
        instrument_header_output += f"  DESCRIPTION = '{odfutils.check_string(self.description)}'\n"
        return instrument_header_output


def main():
    instrument_header = InstrumentHeader()
    print(instrument_header.print_object())
    instrument_header.instrument_type = 'CTD'
    instrument_header.model = 'SBE 9'
    instrument_header.serial_number = '12345'
    instrument_header.log_instrument_message('description', instrument_header.description, 'SeaBird CTD')
    instrument_header.description = 'SeaBird CTD'
    print(instrument_header.print_object())
    for log_entry in BaseHeader.shared_log_list:
        print(log_entry)


if __name__ == "__main__":
    main()
