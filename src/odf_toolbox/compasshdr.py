from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class CompassCalHeader(BaseModel, BaseHeader):
    
    def __init__(self, 
                 parameter_code: str = '',
                 calibration_date: str = '',
                 application_date: str = '',
                 directions: list = [],
                 corrections: list = []):
        super().__init__()        
        self.parameter_code = parameter_code
        self.calibration_date = calibration_date
        self.application_date = application_date
        self.directions = directions
        self.corrections = corrections

    def log_compass_message(self, field: str, old_value: str, new_value: str) -> NoReturn:
        message = f"In Compass Cal Header field {field.upper()} was changed from '{old_value}' to '{new_value}'"
        super().log_message(message)

    @property
    def parameter_code(self) -> str:
        return self._parameter_code

    @parameter_code.setter
    def parameter_code(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._parameter_code = value

    @property
    def calibration_date(self) -> str:
        return self._calibration_date

    @calibration_date.setter
    def calibration_date(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._calibration_date = value.upper()

    @property
    def application_date(self) -> str:
        return self._application_date

    @application_date.setter
    def application_date(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._application_date = value.upper()

    @property
    def directions(self) -> list:
        return self._directions

    @directions.setter
    def directions(self, direction_list: list) -> NoReturn:
        self._directions = direction_list

    def set_direction(self, direction_list: list, direction_number: int = 0) -> NoReturn:
        number_of_directions = len(self.directions)
        if direction_number == 0 and number_of_directions > 0:
            self._directions.extend(direction_list)
        elif direction_number <= number_of_directions and number_of_directions > 0:
            if len(direction_list) == 1:
                self._directions[direction_number] = direction_list.pop()
        else:
            raise ValueError("The 'direction_number' does not match the number of DIRECTIONS.")

    @property
    def corrections(self) -> list:
        return self._corrections

    @corrections.setter
    def corrections(self, correction_list: list) -> NoReturn:
        self._corrections = correction_list

    def set_correction(self, correction_list: list, correction_number: int = 0) -> NoReturn:
        number_of_corrections = len(self.corrections)
        if correction_number == 0 and number_of_corrections > 0:
            self._corrections.extend(correction_list)
        elif correction_number <= number_of_corrections and number_of_corrections > 0:
            if len(correction_list) == 1:
                self._corrections[correction_number] = correction_list.pop()
        else:
            raise ValueError("The 'correction_number' does not match the number of CORRECTIONS.")

    def populate_object(self, compass_cal_fields: list):
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
        compass_cal_header_output += f"  PARAMETER_CODE = '{odfutils.check_string(self.parameter_code)}'\n"
        compass_cal_header_output += f"  CALIBRATION_DATE = '{odfutils.check_datetime(self.calibration_date)}'\n"
        compass_cal_header_output += f"  APPLICATION_DATE = '{odfutils.check_datetime(self.application_date)}'\n"
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
    compass_cal_header = CompassCalHeader()
    print(compass_cal_header.print_object())
    compass_cal_fields = ["PARAMETER_NAME = PARAMETER_CODE",
                        "PARAMETER_CODE = SOG",
                        "CALIBRATION_DATE = 25-mar-2021 00:00:00.00",
                        "APPLICATION_DATE = 25-Mar-2021 00:00:00.00",
                        "DIRECTIONS = 0.0 90.0 180.0 270.0",
                        "CORRECTIONS = 0.0 0.0 0.0 0.0"]
    compass_cal_header.populate_object(compass_cal_fields)
    print(compass_cal_header.print_object())

if __name__ == "__main__":
    main()