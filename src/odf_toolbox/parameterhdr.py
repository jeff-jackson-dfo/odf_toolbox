from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel
class ParameterHeader(BaseModel, BaseHeader):
    """
    A class to represent a Parameter Header in an ODF object.

    Attributes:
    -----------
    _type : string
        the data type of the parameter
    _name : string
        the name of the parameter
    _units : string
        the units of the parameter
    _code : string
        the code of the parameter
    _wmo_code : string
        the wmo code of the parameter
    _null_value : string
        the null value of the parameter
    _print_field_order : integer
        the order of the parameter within the ODF object
    _print_field_width : integer
        the print width for the parameter's values
    _print_decimal_places : integer
        the number of decimal places for the parameter's values
    _angle_of_section : float
    _magnetic_variation : float
    _depth : float
    _minimum_value : not restricted but normally float or str (datetime)
        the minimum value of the parameter
    _maximum_value : not restricted but normally float or str (datetime)
        the maximum value of the parameter
    _number_valid : integer
        the number of valid parameter values
    _number_null : integer
        the number of null parameter values

    Methods:
    -------
    __init__ :
        initialize a ParameterHeader class object
    __str__ : str
        returns a ParameterHeader class object as a string
    """

    def __init__(self,
                 type: str = '',
                 name: str = '',
                 units: str = '',
                 code: str = '',
                 wmo_code: str = '',
                 null_string: str = '',
                 print_field_order: int = None,
                 print_field_width: int = None,
                 print_decimal_places: int = None,
                 angle_of_section: float = None,
                 magnetic_variation: float = None,
                 depth: float = None,
                 minimum_value = None,
                 maximum_value = None,
                 number_valid: int = None,
                 number_null: int = None
                ):

        super().__init__()
        self._type = type
        self._name = name
        self._units = units
        self._code = code
        self._wmo_code = wmo_code
        self._null_string = null_string
        self._print_field_order = print_field_order
        self._print_field_width = print_field_width
        self._print_decimal_places = print_decimal_places
        self._angle_of_section = angle_of_section
        self._magnetic_variation = magnetic_variation
        self._depth = depth
        self._minimum_value = minimum_value
        self._maximum_value = maximum_value
        self._number_valid = number_valid
        self._number_null = number_null

    def log_parameter_message(self, field: str, old_value: str, new_value: str) -> NoReturn:
        message = f"In Parameter Header field {field.upper()} was changed from '{old_value}' to '{new_value}'"
        super().log_message(message)

    def __str__(self):
        return (f'Parameter named "{self.get_name()}" has code "{self.get_code()}", type "{self.get_type()}'
                f'", and units "{self.get_units()}".')

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._type = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._name = value

    @property
    def units(self) -> str:
        return self._units

    @units.setter
    def units(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._units = value

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._code = value

    @property
    def wmo_code(self) -> str:
        return self._wmo_code

    @wmo_code.setter
    def wmo_code(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._wmo_code = value

    @property
    def null_string(self) -> str:
        return self._null_string

    @null_string.setter
    def null_string(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        # if self.type == 'SYTM':
        #     value = '17-NOV-1858 00:00:00.00'
        self._null_string = value

    @property
    def print_field_order(self) -> int:
        return self._print_field_order

    @print_field_order.setter
    def print_field_order(self, value: int) -> NoReturn:
        self._print_field_order = value

    @property
    def print_field_width(self) -> int:
        return self._print_field_width

    @print_field_width.setter
    def print_field_width(self, value: int) -> NoReturn:
        self._print_field_width = value

    @property
    def print_decimal_places(self) -> int:
        return self._print_decimal_places

    @print_decimal_places.setter
    def print_decimal_places(self, value: int) -> NoReturn:
        self._print_decimal_places = value

    @property
    def angle_of_section(self) -> float:
        return self._angle_of_section

    @angle_of_section.setter
    def angle_of_section(self, value: float) -> NoReturn:
        self._angle_of_section = value

    @property
    def magnetic_variation(self) -> float:
        return self._magnetic_variation

    @magnetic_variation.setter
    def magnetic_variation(self, value: float) -> NoReturn:
        self._magnetic_variation = value

    @property
    def depth(self) -> float:
        return self._depth

    @depth.setter
    def depth(self, value: float) -> NoReturn:
        self._depth = value

    @property
    def minimum_value(self):
        return self._minimum_value

    @minimum_value.setter
    def minimum_value(self, value) -> NoReturn:
        self._minimum_value = value

    @property
    def maximum_value(self):
        return self._maximum_value

    @maximum_value.setter
    def maximum_value(self, value) -> NoReturn:
        self._maximum_value = value

    @property
    def number_valid(self) -> int:
        return self._number_valid

    @number_valid.setter
    def number_valid(self, value: int) -> NoReturn:
        self._number_valid = value

    @property
    def number_null(self) -> int:
        return self._number_null

    @number_null.setter
    def number_null(self, value: int) -> NoReturn:
        self._number_null = value

    def populate_object(self, parameter_fields: list) -> NoReturn:
        for header_line in parameter_fields:
            tokens = header_line.split('=', maxsplit=1)
            parameter_dict = odfutils.list_to_dict(tokens)
            for key, value in parameter_dict.items():
                key = key.strip()
                value = value.strip()
                match key:
                    case 'TYPE':
                        self.type = value
                    case 'NAME':
                        self.name = value
                    case 'UNITS':
                        self.units = value
                    case 'CODE':
                        self.code = value
                    case 'WMO_CODE':
                        self.wmo_code = value
                        # If there was no code field in the ODF file being read then assign it the same value as WMO_CODE.
                        if self.code == "":
                            self.code = value
                    case 'NULL_VALUE':
                        self.null_string = value
                    case 'PRINT_FIELD_ORDER':
                        self.print_field_order = int(float(value))
                    case 'PRINT_FIELD_WIDTH':
                        self.print_field_width = int(float(value))
                    case 'PRINT_DECIMAL_PLACES':
                        self.print_decimal_places = int(float(value))
                    case 'ANGLE_OF_SECTION':
                        self.angle_of_section = float(value)
                    case 'MAGNETIC_VARIATION':
                        self.magnetic_variation = float(value)
                    case 'DEPTH':
                        new_value = odfutils.check_string(value)
                        value = float(new_value)
                        self.depth = value
                    case 'MINIMUM_VALUE':
                        if str(value):
                            self.minimum_value = value
                        elif float(value):
                            self.minimum_value = float(value)
                        else:
                            self.minimum_value = BaseHeader.NULL_VALUE
                    case 'MAXIMUM_VALUE':
                        if str(value):
                            self.minimum_value = value
                        elif float(value):
                            self.minimum_value = float(value)
                        else:
                            self.maximum_value = BaseHeader.NULL_VALUE
                    case 'NUMBER_VALID':
                        self.number_valid = int(float(value))
                    case 'NUMBER_NULL':
                        self.number_null = int(float(value))
        return self

    def print_object(self, file_version: float = 2.0) -> str:
        assert file_version >= 2.0, f"File version must be >= 2.0 but is: {file_version}"
        parameter_header_output = "PARAMETER_HEADER\n"
        parameter_header_output += f"  TYPE = '{self.type}'\n"
        parameter_header_output += f"  NAME = '{self.name}'\n"
        parameter_header_output += f"  UNITS = '{self.units}'\n"
        parameter_header_output += f"  CODE = '{self.code}'\n"
        if self._wmo_code != '':
            parameter_header_output += f"  WMO_CODE = '{self.wmo_code}'\n"
        if self._type == "SYTM":
            parameter_header_output += f"  NULL_VALUE = '{odfutils.check_datetime(self.null_string)}'\n"
        else:
            parameter_header_output += f"  NULL_VALUE = {self.null_string}\n"
        if file_version == 3:
            parameter_header_output += (f"  PRINT_FIELD_ORDER = "
                                        f"{self.print_field_order}\n")
        parameter_header_output += f"  PRINT_FIELD_WIDTH = {self.print_field_width}\n"
        parameter_header_output += (f"  PRINT_DECIMAL_PLACES = "
                                    f"{self.print_decimal_places}\n")
        parameter_header_output += (f"  ANGLE_OF_SECTION = "
                                    f"{self.angle_of_section:.1f}\n")
        parameter_header_output += (f"  MAGNETIC_VARIATION = "
                                    f"{self.magnetic_variation:.1f}\n")
        parameter_header_output += f"  DEPTH = {self.depth:.1f}\n"
        if self._units == "GMT" or self._units == "UTC" or self.type == "SYTM":
            parameter_header_output += f"  MINIMUM_VALUE = '{odfutils.check_datetime(self.minimum_value)}'\n"
            parameter_header_output += f"  MAXIMUM_VALUE = '{odfutils.check_datetime(self.maximum_value)}'\n"
        else:
            if self.minimum_value is None:
                parameter_header_output += (f"  MINIMUM_VALUE = {BaseHeader.NULL_VALUE}\n")
            else:
                parameter_header_output += (f"  MINIMUM_VALUE = {float(self.minimum_value):.4f}\n")
            if self.maximum_value is None:
                parameter_header_output += (f"  MAXIMUM_VALUE = {BaseHeader.NULL_VALUE}\n")
            else:
                parameter_header_output += (f"  MAXIMUM_VALUE = {float(self.maximum_value):.4f}\n")
        parameter_header_output += f"  NUMBER_VALID = {self.number_valid}\n"
        parameter_header_output += f"  NUMBER_NULL = {self.number_null}\n"
        return parameter_header_output


def main():
    param = ParameterHeader()
    param.type = 'DOUB'
    param.name = 'Pressure'
    param.units = 'decibars'
    param.code = 'PRES_01'
    param.wmo_code = 'PRES'
    param.null_string = f'{BaseHeader.NULL_VALUE}'
    param.print_field_width = 10
    param.print_decimal_places = 3
    param.angle_of_section = 0.0
    param.magnetic_variation = 0.0
    depth = odfutils.check_string('0.00000000D+00')
    param.depth = float(depth)
    param.minimum_value = 2.177
    param.maximum_value = 176.5
    param.number_valid = 1064
    param.number_null = 643
    param.number_valid = 1064
    print(param.print_object())


if __name__ == "__main__":
    main()
