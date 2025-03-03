from odf_toolbox.basehdr import BaseHeader
from odf_toolbox import odfutils

class InstrumentHeader(BaseHeader):
    """
    A class to represent an Instrument Header in an ODF object.

    Attributes:
    -----------
    InstrumentType : string
        the type of the instrument used to collect the data
    Model : string
        the model of the instrument used to collect the data
    SerialNumber : string
        the units of the data collected by the instrument
    Description : string
        a description of the instrument

    Methods:
    -------
    __init__ :
        initialize a InstrumentHeader class object
    get_instrument_type : string
    set_instrument_type : None
    get_model : string
    set_model : None
    get_serial_number: string
    set_serial_number: None
    get_description: string
    set_description: None

    """

    def __init__(self):
        super().__init__()
        self._instrument_type = ''
        self._model = ''
        self._serial_number = ''
        self._description = ''

    def log_message(self, message):
        super().log_message(f"INSTRUMENT_HEADER: {message}")

    def get_instrument_type(self) -> str:
        return self._instrument_type

    def set_instrument_type(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'INSTRUMENT_TYPE was changed from "{self._instrument_type}" to "{value}"')
        self._instrument_type = f'{value}'

    def get_model(self) -> str:
        return self._model

    def set_model(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'MODEL was changed from "{self._model}" to "{value}"')
        self._model = f'{value}'

    def get_serial_number(self) -> str:
        return self._serial_number

    def set_serial_number(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'SERIAL_NUMBER was changed from "{self._serial_number}" to "{value}"')
        self._serial_number = f'{value}'

    def get_description(self) -> str:
        return self._description

    def set_description(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'DESCRIPTION was changed from "{self._description}" to "{value}"')
        self._description = f'{value}'

    def populate_object(self, instrument_fields: list):
        assert isinstance(instrument_fields, list), \
               f"Input value is not of type list: {instrument_fields}"
        for header_line in instrument_fields:
            tokens = header_line.split('=', maxsplit=1)
            instrument_dict = odfutils.list_to_dict(tokens)
            for key, value in instrument_dict.items():
                key = key.strip()
                value = value.strip()
                match key:
                    case 'INST_TYPE':
                        self.set_instrument_type(value, read_operation=True)
                    case 'MODEL':
                        self.set_model(value, read_operation=True)
                    case 'SERIAL_NUMBER':
                        self.set_serial_number(value, read_operation=True)
                    case 'DESCRIPTION':
                        self.set_description(value, read_operation=True)
        return self
    
    def print_object(self) -> str:
        instrument_header_output = "INSTRUMENT_HEADER\n"
        instrument_header_output += f"  INST_TYPE = '{odfutils.check_string(self.get_instrument_type())}'\n"
        instrument_header_output += f"  MODEL = '{odfutils.check_string(self.get_model())}'\n"
        instrument_header_output += f"  SERIAL_NUMBER = '{odfutils.check_string(self.get_serial_number())}'\n"
        instrument_header_output += f"  DESCRIPTION = '{odfutils.check_string(self.get_description())}'\n"
        return instrument_header_output
