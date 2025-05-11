from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class GeneralCalHeader(BaseModel, BaseHeader):
    """ A class to represent an General Cal Header in an ODF object. """    
    def __init__(self,
                 parameter_code: str = None,
                 calibration_type: str = None,
                 calibration_date: str = None,
                 application_date: str = None,
                 number_coefficients: int = None,
                 coefficients: list = None,
                 calibration_equation: str = None,
                 calibration_comments: list = None
                 ) -> NoReturn:
        super().__init__()
        self.parameter_code = parameter_code if parameter_code is not None else ''
        self.calibration_type = calibration_type if calibration_type is not None else ''
        self.calibration_date = calibration_date if calibration_date is not None else BaseHeader.SYTM_NULL_VALUE
        self.application_date = application_date if application_date is not None else BaseHeader.SYTM_NULL_VALUE
        self.number_coefficients = number_coefficients if number_coefficients is not None else 0
        self.coefficients = coefficients if coefficients is not None else [] 
        self.calibration_equation = calibration_equation if calibration_equation is not None else ''
        self.calibration_comments = calibration_comments if calibration_comments is not None else []

    def log_general_message(self, field: str, old_value: any, new_value: any) -> NoReturn:
        assert isinstance(field, str), "Input argument 'field' must be a string."
        message = f"In General Cal Header field {field.upper()} was changed from '{old_value}' to '{new_value}'"
        super().log_message(message)

    @property
    def parameter_code(self) -> str:
        return self._parameter_code

    @parameter_code.setter
    def parameter_code(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("\' ")
        self._parameter_code = value.upper()

    @property
    def calibration_type(self) -> str:
        return self._calibration_type

    @calibration_type.setter
    def calibration_type(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("\' ")
        self._calibration_type = value

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
    def number_coefficients(self) -> int:
        return self._number_coefficients

    @number_coefficients.setter
    def number_coefficients(self, value: int) -> NoReturn:
        assert isinstance(value, int), "Input argument 'value' must be an integer."
        self._number_coefficients = value

    @property
    def coefficients(self) -> list:
        return self._coefficients

    @coefficients.setter
    def coefficients(self, general_coefficient_list: list):
        assert isinstance(general_coefficient_list, list), "Input argument 'general_coefficient_list' must be a list."
        for coef in general_coefficient_list:
            assert isinstance(coef, float), \
                "Input argument 'general_coefficient_list' must only contain float values."
        self._number_coefficients = len(general_coefficient_list)
        self._coefficients = general_coefficient_list

    def set_coefficient(self, general_coefficient: float, general_coefficient_number: int = 0) -> NoReturn:
        assert isinstance(general_coefficient, float), "Input argument 'general_coefficient' must be a float."
        assert isinstance(general_coefficient_number, int), "Input argument 'general_coefficient' must be a float."
        assert general_coefficient_number >= 0, "The argument 'general_coefficient_number' must be >= 0."
        assert general_coefficient_number <= self.number_coefficients, \
            "The argument 'general_coefficient_number' cannot be larger than the number of COEFFICIENTS."
        if general_coefficient_number == 0:
            self._coefficients.append(general_coefficient)
            self._number_coefficients += 1
        elif general_coefficient_number <= self.number_coefficients and self.number_coefficients > 0:
            self._coefficients[general_coefficient_number - 1] = general_coefficient

    @property
    def calibration_equation(self) -> str:
        return self._calibration_equation

    @ calibration_equation.setter
    def calibration_equation(self, value: str) -> NoReturn:
        assert isinstance(value, str), "The argument 'value' must be a string."
        value = value.strip("\' ")
        self._calibration_equation = value

    @property
    def calibration_comments(self) -> list:
        return self._calibration_comments

    @calibration_comments.setter
    def calibration_comments(self, calibration_comments: list) -> NoReturn:
        assert isinstance(calibration_comments, list), "Input argument 'calibration_comments' must be a list."
        for comment in calibration_comments:
            assert isinstance(comment, str), "All values in input argument 'calibration_comments' must be valid strings."
        self._calibration_comments = calibration_comments

    def set_calibration_comment(self, calibration_comment: str, comment_number: int = 0) -> NoReturn:
        assert isinstance("calibration_comment", str), "Input argument 'calibration_comment' must be a string."
        assert isinstance(comment_number, int), "Input argument 'comment_number' must be a integer."
        assert comment_number >= 0, "Input argument 'comment_number' must be >= 0."
        calibration_comment = calibration_comment.strip("\'")
        number_of_comments = len(self.calibration_comments)
        if comment_number == 0:
            self._calibration_comments.append(calibration_comment)
        elif comment_number <= number_of_comments and number_of_comments > 0:
            self._calibration_comments[comment_number - 1] = calibration_comment

    def populate_object(self, general_cal_fields: list):
        assert isinstance(general_cal_fields, list), "Input argument 'general_cal_fields' must be a list."
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
                        self.number_coefficients = value
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
        general_header_output += f"  PARAMETER_CODE = '{self.parameter_code}'\n"
        general_header_output += (f"  CALIBRATION_TYPE = '{self.calibration_type}'\n")
        general_header_output += (f"  CALIBRATION_DATE = '{self.calibration_date}'\n")
        general_header_output += (f"  APPLICATION_DATE = '{self.application_date}'\n")
        general_header_output += (f"  NUMBER_OF_COEFFICIENTS = {self.number_coefficients}\n")
        coefficients_list = self.coefficients
        coefficients_print = ""
        for coefficient in coefficients_list:
            coefficients_print = coefficients_print + "{:.8e}".format(coefficient) + " "
        general_header_output += f"  COEFFICIENTS = {coefficients_print}\n"
        general_header_output += (f"  CALIBRATION_EQUATION = '{self.calibration_equation}'\n")
        for general_comment in self.calibration_comments:
            general_header_output += f"  CALIBRATION_COMMENTS = '{general_comment}'\n"
        return general_header_output


def main():
    print()

    general = GeneralCalHeader()
    print(general.print_object())
    general.parameter_code = 'PSAR_01'
    general.calibration_type = 'Linear'
    general.calibration_date = '28-May-2020 00:00:00.00'
    general.application_date = '14-Oct-2020 23:59:59.99'
    general.number_coefficients = 2
    general.coefficients = [0.75, 1.05834]
    general.calibration_equation = 'y = mx + b'
    general.set_calibration_comment('This is a comment')
    general.log_general_message('calibration_equation', general.calibration_equation, 'Y = X^2 + MX + B')
    general.set_coefficient(3.5, 1)
    print(general.print_object())
    for log_entry in BaseHeader.shared_log_list:
        print(log_entry)
    print()
    
if __name__ == "__main__":
    main()