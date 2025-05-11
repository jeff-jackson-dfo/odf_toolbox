from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class CompassCalHeader(BaseModel, BaseHeader):
    """ A class to represent a Compass Cal Header in an ODF object. """
    
    def __init__(self, 
                 parameter_code: str = None,
                 calibration_date: str = None,
                 application_date: str = None,
                 directions: list = None,
                 corrections: list = None):
        super().__init__()        
        self.parameter_code = parameter_code if parameter_code is not None else ''
        self.calibration_date = calibration_date if calibration_date is not None else BaseHeader.SYTM_NULL_VALUE
        self.application_date = application_date if application_date is not None else BaseHeader.SYTM_NULL_VALUE
        self.directions = directions if directions is not None else []
        self.corrections = corrections if corrections is not None else []

    def log_compass_message(self, field: str, old_value: str, new_value: str) -> NoReturn:
        assert isinstance(field, str), "Input argument 'field' must be a string."
        assert isinstance(old_value, str), "Input argument 'old_value' must be a string."
        assert isinstance(new_value, str), "Input argument 'new_value' must be a string."
        message = f"In Compass Cal Header field {field.upper()} was changed from '{old_value}' to '{new_value}'"
        super().log_message(message)

    @property
    def parameter_code(self) -> str:
        return self._parameter_code

    @parameter_code.setter
    def parameter_code(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        # TODO: Check if the value is a valid parameter code
        # if value not in self.valid_parameter_codes:
        #     raise ValueError(f"Invalid parameter code: {value}")
        value = value.strip("\' ")
        self._parameter_code = value

    @property
    def calibration_date(self) -> str:
        return self._calibration_date

    @calibration_date.setter
    def calibration_date(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = odfutils.check_datetime(value)
        value = value.strip("\' ")
        self._calibration_date = value.upper()

    @property
    def application_date(self) -> str:
        return self._application_date

    @application_date.setter
    def application_date(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = odfutils.check_datetime(value)
        value = value.strip("\' ")
        self._application_date = value.upper()

    @property
    def directions(self) -> list:
        return self._directions

    @directions.setter
    def directions(self, direction_list: list) -> NoReturn:
        assert isinstance(direction_list, list), "Input argument 'direction_list' must be a list."
        for direction in direction_list:
            assert isinstance(direction, float), "Input argument 'direction_list' must only contain float values."
            assert direction >= 0 and direction < 360, \
                "The argument 'direction_list' must have values that are greater than or equal to 0 and less than 360 degrees."
        self._directions = direction_list

    def set_direction(self, direction: float, direction_number: int = 0) -> NoReturn:
        assert isinstance(direction, float), "Input argument 'direction' must be a float."
        assert direction >= 0 and direction < 360, \
            "The argument 'direction' must be greater than or equal to 0 and less than 360 degrees."
        assert isinstance(direction_number, int), "Input argument 'direction_number' must be an int."
        assert direction_number >= 0, "The argument 'direction_number' must be >= 0."
        number_of_directions = len(self.directions)
        if direction_number > number_of_directions:
            "The argument 'direction_number' cannot be greater than the current number of DIRECTIONS."
        if direction_number == 0:
            self._directions.append(direction)
            self._directions += 1
        elif number_of_directions > 0:
            self._directions[direction_number - 1] = direction

    @property
    def corrections(self) -> list:
        return self._corrections

    @corrections.setter
    def corrections(self, correction_list: list) -> NoReturn:
        assert isinstance(correction_list, list), "Input argument 'correction_list' must be a list."
        for correction in correction_list:
            assert isinstance(correction, float), "Input argument 'correction_list' must only contain float values."
            assert correction >= 0 and correction < 360, \
                "The argument 'correction_list' must have values that are greater than or equal to 0 and less than 360."
        self._corrections = correction_list

    def set_correction(self, correction: float, correction_number: int = 0) -> NoReturn:
        assert isinstance(correction, float), "Input argument 'correction' must be a float."
        assert correction >= 0 and correction < 360, \
            "The argument 'correction' must be greater than or equal to 0 and less than 360."
        assert isinstance(correction_number, int), "Input argument 'correction_number' must be an int."
        assert correction_number >= 0, "The argument 'correction_number' must be >= 0."
        number_of_corrections = len(self.corrections)
        assert correction_number <= number_of_corrections, \
             "The argument 'correction_number' cannot be greater than the current number of CORRECTIONS."
        if correction_number == 0:
            self._corrections.append(correction)
            self._corrections += 1
        elif number_of_corrections > 0:
            self._corrections[correction_number - 1] = correction

    def populate_object(self, compass_cal_fields: list):
        assert isinstance(compass_cal_fields, list), "Input argument 'compass_cal_fields' must be a list."
        for header_line in compass_cal_fields:
            tokens = header_line.split('=', maxsplit=1)
            compass_dict = odfutils.list_to_dict(tokens)
            for key, value in compass_dict.items():
                key = key.strip()
                value = value.strip()
                match key:
                    case 'PARAMETER_NAME':
                        self.parameter_code = value
                    case 'PARAMETER_CODE':
                        self.parameter_code = value
                    case 'CALIBRATION_DATE':
                        self.calibration_date = value
                    case 'APPLICATION_DATE':
                        self.application_date = value
                    case 'DIRECTIONS':
                        direction_list = value.split()
                        direction_floats = [float(direction) for direction in direction_list]
                        self.directions = direction_floats
                    case 'CORRECTIONS':
                        correction_list = value.split()
                        correction_floats = [float(correction) for correction in correction_list]
                        self.corrections = correction_floats
        return self

    def print_object(self) -> str:
        compass_cal_header_output = "COMPASS_CAL_HEADER\n"
        compass_cal_header_output += f"  PARAMETER_CODE = '{self.parameter_code}'\n"
        compass_cal_header_output += f"  CALIBRATION_DATE = '{self.calibration_date}'\n"
        compass_cal_header_output += f"  APPLICATION_DATE = '{self.application_date}'\n"
        directions_list = self.directions
        directions_print = ""
        for direction in directions_list:
            directions_print = directions_print + "{:.8e}".format(direction) + " "
        compass_cal_header_output += f"  DIRECTIONS = {directions_print}\n"
        corrections_list = self.corrections
        corrections_print = ""
        for correction in corrections_list:
            corrections_print = corrections_print + "{:.8e}".format(correction) + " "
        compass_cal_header_output += f"  CORRECTIONS = {corrections_print}\n"
        return compass_cal_header_output

def main():
    print()
    compass_cal_header = CompassCalHeader()
    print(compass_cal_header.print_object())
    compass_cal_fields = ["PARAMETER_NAME = PARAMETER_CODE",
                        "PARAMETER_CODE = SOG_01",
                        "CALIBRATION_DATE = 25-mar-2021 00:00:00.00",
                        "APPLICATION_DATE = 31-jan-2022 00:00:00.00",
                        "DIRECTIONS = 0.0 90.0 180.0 270.0",
                        "CORRECTIONS = 70.0 0.0 0.0 0.0"]
    compass_cal_header.populate_object(compass_cal_fields)
    print(compass_cal_header.print_object())
    print()

if __name__ == "__main__":
    main()