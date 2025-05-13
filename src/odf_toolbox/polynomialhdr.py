from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class PolynomialCalHeader(BaseModel, BaseHeader):
    
    def __init__(self,
                 parameter_code: str = None,
                 calibration_date: str = None,
                 application_date: str = None,
                 number_coefficients: int = None,
                 coefficients: list = None
                 ):
        super().__init__()
        self.parameter_code = parameter_code if parameter_code is not None else ''
        self.calibration_date = calibration_date if calibration_date is not None else BaseHeader.SYTM_NULL_VALUE
        self.application_date = application_date if application_date is not None else BaseHeader.SYTM_NULL_VALUE
        self.number_coefficients = number_coefficients if number_coefficients is not None else 0
        self.coefficients = coefficients if coefficients is not None else []

    def log_poly_message(self, field: str, old_value: any, new_value: any) -> NoReturn:
        assert isinstance(field, str), "Input argument 'field' must be a string."
        message = f"In Polynomial Cal Header field {field.upper()} was changed from '{old_value}' to '{new_value}'"
        super().log_message(message)

    @property
    def parameter_code(self) -> str:
        return self._parameter_code

    @parameter_code.setter
    def parameter_code(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("\' ")
        self._parameter_code = value

    @property
    def calibration_date(self) -> str:
        return self._calibration_date

    @calibration_date.setter
    def calibration_date(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("\' ")
        self._calibration_date = odfutils.check_datetime(value)

    @property
    def application_date(self) -> str:
        return self._application_date

    @application_date.setter
    def application_date(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("\' ")
        self._application_date = odfutils.check_datetime(value)

    @property
    def number_coefficients(self) -> int:
        return self._number_coefficients

    @number_coefficients.setter
    def number_coefficients(self, value: int) -> NoReturn:
        assert isinstance(value, int), "Input argument 'value' must be a integer."
        self._number_coefficients = value

    @property
    def coefficients(self) -> list:
        return self._coefficients

    @coefficients.setter
    def coefficients(self, coefficient_list: list):
        assert isinstance(coefficient_list, list), "Input argument 'coefficient_list' must be a list."
        for x, coef in enumerate(coefficient_list):
            assert isinstance(coef, float), "Input argument 'coefficient_list' must be a list of floats."
        self._coefficients = coefficient_list

    def set_coefficient(self, coefficient: float, coefficient_number: int = 0):
        assert isinstance(coefficient, float), "Input argument 'coefficient' must be a float."
        assert isinstance(coefficient_number, int), "Input argument 'coefficient_number' must be a integer."
        assert coefficient_number >= 0, "Input argument 'coefficient_number' must be >= 0."
        assert coefficient_number <= self.number_coefficients, "Input argument 'coefficient_number' must be <= the number of current coefficients."
        if coefficient_number == 0:
            self._coefficients.append(coefficient)
        elif coefficient_number <= self.number_coefficients and self.number_coefficients > 0:
            self._coefficients[coefficient_number - 1] = coefficient

    def populate_object(self, polynomial_cal_fields: list):
        assert isinstance(polynomial_cal_fields, list), f"Input argument 'polynomial_cal_fields' is not of type list."
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
                        for i, coef in enumerate(coefficient_list):
                            if isinstance(coef, str):
                                coefficient_list[i] = odfutils.check_string(coef)
                        self._coefficients = coefficient_list
        return self

    def print_object(self) -> str:
        polynomial_header_output = "POLYNOMIAL_CAL_HEADER\n"
        polynomial_header_output += f"  PARAMETER_CODE = '{self.parameter_code}'\n"
        polynomial_header_output += (f"  CALIBRATION_DATE = "
                                     f"'{odfutils.check_datetime(self.calibration_date)}'\n")
        polynomial_header_output += (f"  APPLICATION_DATE = "
                                     f"'{odfutils.check_datetime(self.application_date)}'\n")
        polynomial_header_output += f"  NUMBER_COEFFICIENTS = {self.number_coefficients}\n"
        coefficients_print = ""
        for coefficient in self.coefficients:
            coefficient = float(coefficient)
            coefficients_print = f"{coefficients_print} {coefficient:.8e}"
        polynomial_header_output += f"  COEFFICIENTS = {coefficients_print}\n"
        return polynomial_header_output


def main():
    print()
    
    poly1 = PolynomialCalHeader()
    print(poly1.print_object())
    poly1.parameter_code = 'PRES_01'
    poly1.calibration_date = '11-JUN-1995 05:35:46.82'
    poly1.application_date = '11-JUN-1995 05:35:46.82'
    poly1.number_coefficients = 2
    poly1.coefficients = [0.60000000e+01,  0.15000001e+00]
    print(poly1.print_object())

    poly2 = PolynomialCalHeader()
    poly2.parameter_code = 'TEMP_01'
    poly2.calibration_date = '11-JUN-1995 05:35:46.83'
    poly2.application_date = '11-JUN-1995 05:35:46.83'
    poly2.number_coefficients = 4
    poly2.coefficients = [0.0, 80.0, 0.60000000e+01,  0.15000001e+00]
    poly2.log_poly_message('coefficient 2', poly2.coefficients[1], 9.750)
    poly2.set_coefficient(9.750, 2)
    print(poly2.print_object())

    for log_entry in BaseHeader.shared_log_list:
        print(log_entry)
    print()
    
if __name__ == "__main__":
    main()