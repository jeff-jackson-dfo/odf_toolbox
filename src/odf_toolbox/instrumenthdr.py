from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class InstrumentHeader(BaseModel, BaseHeader):
    """ A class to represent an Instrument Header in an ODF object. """
    def __init__(self, 
                 instrument_type: str = None, 
                 model: str = None, 
                 serial_number: str = None, 
                 description: str = None
                 ) -> NoReturn:
        super().__init__()
        self.instrument_type = instrument_type if instrument_type is not None else ''
        self.model = model if model is not None else ''
        self.serial_number = serial_number if serial_number is not None else ''
        self.description = description if description is not None else ''

    def log_instrument_message(self, field: str, old_value: str, new_value: str) -> NoReturn:
        assert isinstance(field, str), "Input argument 'field' must be a string."
        assert isinstance(old_value, str), "Input argument 'old_value' must be a string."
        assert isinstance(new_value, str), "Input argument 'new_value' must be a string."
        if old_value == "":
            old_value = "''"
        message = f"In Instrument Header field {field.upper()} was changed from {old_value} to '{new_value}'"
        super().log_message(message)

    @property
    def instrument_type(self) -> str:
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        self._instrument_type = value

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        self._model = value

    @property
    def serial_number(self) -> str:
        return self._serial_number

    @serial_number.setter
    def serial_number(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        self._serial_number = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        self._description = value

    def populate_object(self, instrument_fields: list):
        assert isinstance(instrument_fields, list), "Input argument 'instrument_fields' must be a list."
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
        instrument_header_output += f"  INST_TYPE = '{self.instrument_type}'\n"
        instrument_header_output += f"  MODEL = '{self.model}'\n"
        instrument_header_output += f"  SERIAL_NUMBER = '{self.serial_number}'\n"
        instrument_header_output += f"  DESCRIPTION = '{self.description}'\n"
        return instrument_header_output


def main():
    print()

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
    print()

if __name__ == "__main__":
    main()
