from odf_toolbox import BaseHeader
from odf_toolbox import odfutils

class CompassCalHeader(BaseHeader):
    
    def __init__(self):
        super().__init__()        
        self._parameter_code = ''
        self._calibration_date = ''
        self._application_date = ''
        self._directions = []
        self._corrections = []

    def log_message(self, message):
        super().log_message(f"In Compass Cal Header field {message}")

    def get_parameter_code(self) -> str:
        return self._parameter_code

    def set_parameter_code(self, value: str, read_operation: bool = False) -> None:
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'PARAMETER_CODE was changed from "{self._parameter_code}" to "{value}"')
        self._parameter_code = f'{value}'

    def get_calibration_date(self) -> str:
        return self._calibration_date

    def set_calibration_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'CALIBRATION_DATE was changed from "{self._calibration_date}" to "{value}"')
        self._calibration_date = f'{value}'

    def get_application_date(self) -> str:
        return self._application_date

    def set_application_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'APPLICATION_DATE was changed from "{self._application_date}" to "{value}"')
        self._application_date = f'{value}'

    def get_directions(self) -> list:
        return self._directions

    def set_directions(self, direction_list: list, direction_number: int = 0, read_operation: bool = False) -> None:
        assert isinstance(direction_list, list), \
               f"Input value is not of type list: {direction_list}"
        assert isinstance(direction_number, int), \
               f"Input value is not of type int: {direction_number}"
        number_of_directions = len(self.get_directions())
        if direction_number == 0 and number_of_directions == 0:
            if not read_operation:
                self.log_message(f'The following set of directions was added to Compass_Cal_Header.Directions: {direction_list}')
            self._directions = direction_list
        elif direction_number == 0 and number_of_directions > 0:
            if not read_operation:
                self.log_message(f"The following set of directions was added to Compass_Cal_Header.Directions: {direction_list}")
            self._directions.extend(direction_list)
        elif direction_number <= number_of_directions and number_of_directions > 0:
            if len(direction_list) == 1:
                if not read_operation:
                    self.log_message(f"DIRECTION {direction_list.pop()} in Compass_Cal_Header.Directions was "
                                         f"changed from {self._directions[direction_number - 1]} "
                                         f"to {direction_list.pop()}")
                self._directions[direction_number] = direction_list.pop()
        else:
            raise ValueError("The 'direction_number' does not match the number of DIRECTIONS.")

    def get_corrections(self) -> list:
        return self._corrections

    def set_corrections(self, correction_list: list, correction_number: int = 0, read_operation: bool = False) -> None:
        assert isinstance(correction_list, list), \
               f"Input value is not of type list: {correction_list}"
        assert isinstance(correction_number, int), \
               f"Input value is not of type int: {correction_number}"
        number_of_corrections = len(self.get_corrections())
        if correction_number == 0 and number_of_corrections == 0:
            if not read_operation:
                self.log_message(f"The following set of corrections was added to Compass_Cal_Header.Corrections: {correction_list}")
            self._corrections = correction_list
        elif correction_number == 0 and number_of_corrections > 0:
            if not read_operation:
                self.log_message(f"The following set of corrections was added to Corrections: {correction_list}")
            self._corrections.extend(correction_list)
        elif correction_number <= number_of_corrections and number_of_corrections > 0:
            if len(correction_list) == 1:
                if not read_operation:
                    self.log_message(f"CORRECTION {correction_list.pop()} in Compass_Cal_Header.Corrections was "
                                         f"changed from {self._corrections[correction_number - 1]} "
                                         f"to '{correction_list.pop()}'")
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
                        self.set_parameter_code(value, read_operation=True)
                    case 'PARAMETER_CODE':
                        self.set_parameter_code(value, read_operation=True)
                    case 'CALIBRATION_DATE':
                        self.set_calibration_date(value, read_operation=True)
                    case 'APPLICATION_DATE':
                        self.set_application_date(value, read_operation=True)
                    case 'DIRECTIONS':
                        direction_list = value.split()
                        direction_floats = [float(direction) for direction in direction_list]
                        self.set_directions(direction_floats, read_operation=True)
                    case 'CORRECTIONS':
                        correction_list = value.split()
                        correction_floats = [float(correction) for correction in correction_list]
                        self.set_corrections(correction_floats, read_operation=True)
        return self

    def print_object(self) -> str:
        compass_cal_header_output = "COMPASS_CAL_HEADER\n"
        compass_cal_header_output += f"  PARAMETER_CODE = '{odfutils.check_string(self.get_parameter_code())}'\n"
        compass_cal_header_output += f"  CALIBRATION_DATE = '{odfutils.check_datetime(self.get_calibration_date())}'\n"
        compass_cal_header_output += f"  APPLICATION_DATE = '{odfutils.check_datetime(self.get_application_date())}'\n"
        directions_list = self.get_directions()
        directions_print = ""
        for direction in directions_list:
            directions_print = directions_print + "{:.8e}".format(direction) + " "
        compass_cal_header_output += f"  DIRECTIONS = {directions_print}\n"
        corrections_list = self.get_corrections()
        corrections_print = ""
        for correction in corrections_list:
            corrections_print = corrections_print + "{:.8e}".format(correction) + " "
        compass_cal_header_output += f"  CORRECTIONS = {corrections_print}\n"
        return compass_cal_header_output

    def main():
        compass_cal_header = CompassCalHeader()
        compass_cal_fields = ["PARAMETER_NAME = 'PARAMETER_CODE'",
                            "PARAMETER_CODE = 'SOG'",
                            "CALIBRATION_DATE = '2021-03-25T00:00:00'",
                            "APPLICATION_DATE = '2021-03-25T00:00:00'",
                            "DIRECTIONS = 0.0 90.0 180.0 270.0",
                            "CORRECTIONS = 0.0 0.0 0.0 0.0"]
        compass_cal_header.populate_object(compass_cal_fields)
        print(compass_cal_header.print_object())

if __name__ == "__main__":

    CompassCalHeader.main()