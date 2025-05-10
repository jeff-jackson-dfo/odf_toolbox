from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class GeneralCalHeader(BaseModel, BaseHeader):
    
    def __init__(self,
                 parameter_code: str = '',
                 calibration_type: str = '',
                 calibration_date: str = BaseHeader.SYTM_NULL_VALUE,
                 application_date: str = BaseHeader.SYTM_NULL_VALUE,
                 number_coefficients: int = 0,
                 coefficients: list = None,
                 calibration_equation: str = '',
                 calibration_comments: list = None
                 ):
        super().__init__()
        self.parameter_code = parameter_code
        self.calibration_type = calibration_type
        self.calibration_date = calibration_date
        self.application_date = application_date
        self.number_coefficients = number_coefficients
        self.coefficients = coefficients if coefficients is not None else [] 
        self.calibration_equation = calibration_equation
        self.calibration_comments = calibration_comments if calibration_comments is not None else []

    def log_general_message(self, field: str, old_value: str, new_value: str) -> NoReturn:
        message = f"In General Cal Header field {field.upper()} was changed from '{old_value}' to '{new_value}'"
        super().log_message(message)

    @property
    def parameter_code(self) -> str:
        return self._parameter_code

    @parameter_code.setter
    def parameter_code(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._parameter_code = value.upper()

    @property
    def calibration_type(self) -> str:
        return self._calibration_type

    @calibration_type.setter
    def calibration_type(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._calibration_type = value

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
    def number_coefficients(self) -> int:
        return self._number_coefficients

    @number_coefficients.setter
    def number_coefficients(self, value: int) -> NoReturn:
        self._number_coefficients = value

    @property
    def coefficients(self) -> list:
        return self._coefficients

    @coefficients.setter
    def coefficients(self, general_coefficient_list: list):
        self._coefficients = general_coefficient_list

    def set_coefficient(self, general_coefficient_list: list, general_coefficient_number: int = 0) -> NoReturn:
        number_of_general_coefficients = self.get_number_coefficients()
        if number_of_general_coefficients > 0:
            self._coefficients.extend(general_coefficient_list)
        elif general_coefficient_number <= number_of_general_coefficients and number_of_general_coefficients > 0:
            if len(general_coefficient_list) == 1:
                self._coefficients[general_coefficient_number] = general_coefficient_list.pop()
        else:
            raise ValueError("The 'coefficient_number' does not match the number of COEFFICIENTS.")

    @property
    def calibration_equation(self) -> str:
        return self._calibration_equation

    @ calibration_equation.setter
    def calibration_equation(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._calibration_equation = value

    @property
    def calibration_comments(self) -> list:
        return self._calibration_comments

    @calibration_comments.setter
    def calibration_comments(self, calibration_comments: list) -> NoReturn:
        self._calibration_comments = calibration_comments

    def set_calibration_comment(self, calibration_comment: str, comment_number: int = 0) -> NoReturn:
        calibration_comment = calibration_comment.strip("\'")
        number_of_comments = len(self.calibration_comments)
        if comment_number == 0 and number_of_comments >= 0:
            self._calibration_comments.append(calibration_comment)
        elif comment_number <= number_of_comments and number_of_comments > 0:
            self._calibration_comments[comment_number] = calibration_comment
        else:
            raise ValueError("The 'calibration_comment' number does not match " \
                             "the number of CALIBRATION_COMMENTS lines.")

    def populate_object(self, general_cal_fields: list):
        for header_line in general_cal_fields:
            tokens = header_line.split('=', maxsplit=1)
            general_dict = odfutils.list_to_dict(tokens)
            for key, value in general_dict.items():
                key = key.strip()
                value = value.strip()
                match key:
                    case 'PARAMETER_CODE':
                        self.parameter_code = value
                    case 'CALIBRATION_TYPE':
                        self.calibration_type = value
                    case 'CALIBRATION_DATE':
                        self.calibration_date = value
                    case 'APPLICATION_DATE':
                        self.application_date = value
                    case 'NUMBER_OF_COEFFICIENTS':
                        self.number_coefficients = int(value)
                    case 'COEFFICIENTS':
                        coefficient_list = value.split()
                        coefficient_floats = [float(coefficient) for coefficient in coefficient_list]
                        self.coefficients = coefficient_floats
                    case 'CALIBRATION_EQUATION':
                        self.calibration_equation = value
                    case 'CALIBRATION_COMMENTS':
                        self.calibration_comments = value
        return self

    # noinspection DuplicatedCode
    def print_object(self) -> str:
        general_header_output = "GENERAL_CAL_HEADER\n"
        general_header_output += f"  PARAMETER_CODE = '{odfutils.check_string(self.parameter_code)}'\n"
        general_header_output += (f"  CALIBRATION_TYPE = '{odfutils.check_string(self.calibration_type)}'\n")
        general_header_output += (f"  CALIBRATION_DATE = '{odfutils.check_datetime(self.calibration_date)}'\n")
        general_header_output += (f"  APPLICATION_DATE = '{odfutils.check_datetime(self.application_date)}'\n")
        general_header_output += (f"  NUMBER_OF_COEFFICIENTS = {odfutils.check_int(self.number_coefficients)}\n")
        coefficients_list = self.coefficients
        coefficients_print = ""
        for coefficient in coefficients_list:
            coefficients_print = coefficients_print + "{:.8e}".format(coefficient) + " "
        general_header_output += f"  COEFFICIENTS = {coefficients_print}\n"
        general_header_output += (f"  CALIBRATION_EQUATION = '{odfutils.check_string(self.calibration_equation)}'\n")
        for general_comment in self.calibration_comments:
            general_header_output += f"  CALIBRATION_COMMENTS = '{general_comment}'\n"
        return general_header_output


def main():
    general = GeneralCalHeader()
    print(general.print_object())
    general.parameter_code = 'PAR'
    general.calibration_type = 'Linear'
    general.calibration_date = '28-May-2020 00:00:00.00'
    general.application_date = '14-Oct-2020 23:59:59.99'
    general.number_coefficients = 2
    general.coefficients = [0.75, 1.05834]
    general.calibration_equation = 'y = mx + b'
    general.set_calibration_comment('This is a comment')
    general.log_general_message('calibration_equation', general.calibration_equation, 'Y = X^2 + MX + B')
    print(general.print_object())
    for log_entry in BaseHeader.shared_log_list:
        print(log_entry)

if __name__ == "__main__":
    main()