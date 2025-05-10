from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class PolynomialCalHeader(BaseModel, BaseHeader):
    
    def __init__(self,
                 parameter_code: str = '',
                 calibration_date: str = BaseHeader.SYTM_NULL_VALUE,
                 application_date: str = BaseHeader.SYTM_NULL_VALUE,
                 number_coefficients: int = 0,
                 coefficients: list = None
                 ):
        super().__init__()
        self.parameter_code = parameter_code
        self.calibration_date = calibration_date
        self.application_date = application_date
        self.number_coefficients = number_coefficients
        self.coefficients = coefficients if coefficients is not None else []

    def log_poly_message(self, field: str, old_value: str, new_value: str) -> NoReturn:
        message = f"In Polynomial Cal Header field {field.upper()} was changed from '{old_value}' to '{new_value}'"
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
        self._calibration_date = value

    @property
    def application_date(self) -> str:
        return self._application_date

    @application_date.setter
    def application_date(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._application_date = value

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
    def coefficients(self, coefficient_list: list):
        self._coefficients = coefficient_list

    def set_coefficient(self, coefficient_list: list, coefficient_number: int = 0):
        number_coefficients = self.get_number_coefficients()
        for idx, coefficient in enumerate(coefficient_list):
            new_coefficient = odfutils.check_string(coefficient)
            coefficient_list[idx] = odfutils.check_float(float(new_coefficient))
        if coefficient_number == 0 and number_coefficients == 0:
            self._coefficients = coefficient_list
        elif coefficient_number == 0 and number_coefficients > 0:
            self._coefficients.extend(coefficient_list)
        elif coefficient_number <= number_coefficients and number_coefficients > 0:
            if len(coefficient_list) == 1:
                self._coefficients[coefficient_number] = coefficient_list.pop()
        else:
            raise ValueError("The 'coefficient_number' does not match the number of COEFFICIENTS.")

    def populate_object(self, polynomial_cal_fields: list):
        assert isinstance(polynomial_cal_fields, list), \
               f"Input value is not of type list: {polynomial_cal_fields}"
        for header_line in polynomial_cal_fields:
            tokens = header_line.split('=', maxsplit=1)
            poly_dict = odfutils.list_to_dict(tokens)
            for key, value in poly_dict.items():
                key = key.strip()
                value = value.strip("' ")
                match key:
                    case 'PARAMETER_NAME':
                        self._parameter_code = value
                    case 'PARAMETER_CODE':
                        self._parameter_code = value
                    case 'CALIBRATION_DATE':
                        self._calibration_date = value
                    case 'APPLICATION_DATE':
                        self._application_date = value
                    case 'NUMBER_OF_COEFFICIENTS':
                        value = int(value)
                        self._number_coefficients = value
                    case 'COEFFICIENTS':
                        coefficient_list = value.split()
                        self._coefficients = coefficient_list
        return self

    def print_object(self) -> str:
        polynomial_header_output = "POLYNOMIAL_CAL_HEADER\n"
        polynomial_header_output += f"  PARAMETER_CODE = '{odfutils.check_string(self.parameter_code)}'\n"
        polynomial_header_output += (f"  CALIBRATION_DATE = "
                                     f"'{odfutils.check_datetime(self.calibration_date)}'\n")
        polynomial_header_output += (f"  APPLICATION_DATE = "
                                     f"'{odfutils.check_datetime(self.application_date)}'\n")
        polynomial_header_output += f"  NUMBER_COEFFICIENTS = {self.number_coefficients}\n"
        coefficients_list = self.coefficients
        coefficients_print = ""
        for coefficient in coefficients_list:
            coefficient = float(odfutils.check_string(coefficient))
            coefficients_print = coefficients_print + "{:.8e}".format(coefficient) + " "
        polynomial_header_output += f"  COEFFICIENTS = {coefficients_print}\n"
        return polynomial_header_output


def main():
    poly1 = PolynomialCalHeader()
    print(poly1.print_object())
    poly1.parameter_code = 'PRES_01'
    poly1.calibration_date = '11-JUN-1995 05:35:46.82'
    poly1.application_date = '11-JUN-1995 05:35:46.82'
    poly1.number_coefficients = 2
    poly1.coefficients = ['0.60000000D+01',  '0.15000001D+00']
    print(poly1.print_object())

    poly2 = PolynomialCalHeader()
    poly2.parameter_code = 'TEMP_01'
    poly2.calibration_date = '11-JUN-1995 05:35:46.83'
    poly2.application_date = '11-JUN-1995 05:35:46.83'
    poly2.number_coefficients = 2
    poly2.coefficients = ['0.00000000E+01',  '0.25000001E-03']
    print(poly2.print_object())

if __name__ == "__main__":
    main()