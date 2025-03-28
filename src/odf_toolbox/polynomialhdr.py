from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
class PolynomialCalHeader(BaseHeader):
    
    def __init__(self):
        super().__init__()
        self._parameter_code = None
        self._calibration_date = None
        self._application_date = None
        self._number_coefficients = 0
        self._coefficients = []

    def log_message(self, message):
        super().log_message(f"In Polynomial Cal Header field {message}")

    def get_parameter_code(self) -> str:
        return self._parameter_code

    def set_parameter_code(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f"PARAMETER_CODE was changed from "
                                 f"'{self._parameter_code}' to '{value}'")
        self._parameter_code = f"{value}"

    def get_calibration_date(self) -> str:
        return self._calibration_date

    def set_calibration_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f"CALIBRATION_DATE was changed from "
                                 f"'{self._calibration_date}' to '{value}'")
        self._calibration_date = f"{value}"

    def get_application_date(self) -> str:
        return self._application_date

    def set_application_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f"APPLICATION_DATE was changed from "
                                 f"{self._application_date} to '{value}'")
        self._application_date = f"{value}"

    def get_number_coefficients(self) -> int:
        return self._number_coefficients

    def set_number_coefficients(self, value: int, read_operation: bool = False) -> None:
        assert isinstance(value, int), \
               f"Input value is not of type int: {value}"
        if not read_operation:
            self.log_message(f"NUMBER_COEFFICIENTS was changed from "
                                 f"{self._number_coefficients} to {value}")
        self._number_coefficients = value

    def get_coefficients(self) -> list:
        return self._coefficients

    def set_coefficients(self, coefficient_list: list, coefficient_number: int = 0, read_operation: bool = False):
        assert isinstance(coefficient_list, list), \
               f"Input value is not of type list: {coefficient_list}"
        assert isinstance(coefficient_number, int), \
               f"Input value is not of type int: {coefficient_number}"
        number_coefficients = self.get_number_coefficients()
        for idx, coefficient in enumerate(coefficient_list):
            new_coefficient = odfutils.check_string(coefficient)
            coefficient_list[idx] = odfutils.check_float(float(new_coefficient))
            coefficient_list[idx]
        if coefficient_number == 0 and number_coefficients == 0:
            if not read_operation:
                self.log_message(f"The following set of COEFFICIENTS was added : {coefficient_list}")
            self._coefficients = coefficient_list
        elif coefficient_number == 0 and number_coefficients > 0:
            if not read_operation:
                self.log_message(f"The following set of COEFFICIENTS was added : {coefficient_list}")
            self._coefficients.extend(coefficient_list)
        elif coefficient_number <= number_coefficients and number_coefficients > 0:
            if len(coefficient_list) == 1:
                if not read_operation:
                    self.log_message(f"Coefficient {coefficient_list.pop()} in "
                                         f"COEFFICIENTS was "
                                         f"changed from {self._coefficients[coefficient_number - 1]} "
                                         f"to {coefficient_list.pop()}")
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
                    case 'NUMBER_OF_COEFFICIENTS':
                        value = int(value)
                        self.set_number_coefficients(value, read_operation=True)
                    case 'COEFFICIENTS':
                        coefficient_list = value.split()
                        self.set_coefficients(coefficient_list, read_operation=True)
        return self

    def print_object(self) -> str:
        polynomial_header_output = "POLYNOMIAL_CAL_HEADER\n"
        polynomial_header_output += f"  PARAMETER_CODE = '{odfutils.check_string(self.get_parameter_code())}'\n"
        polynomial_header_output += (f"  CALIBRATION_DATE = "
                                     f"'{odfutils.check_datetime(self.get_calibration_date())}'\n")
        polynomial_header_output += (f"  APPLICATION_DATE = "
                                     f"'{odfutils.check_datetime(self.get_application_date())}'\n")
        polynomial_header_output += (f"  NUMBER_COEFFICIENTS = "
                                     f"{odfutils.check_int(self.get_number_coefficients())}\n")
        coefficients_list = self.get_coefficients()
        coefficients_print = ""
        for coefficient in coefficients_list:
            coefficients_print = coefficients_print + "{:.8e}".format(coefficient) + " "
        polynomial_header_output += f"  COEFFICIENTS = {coefficients_print}\n"
        return polynomial_header_output


    def main():
        poly1 = PolynomialCalHeader()
        poly1.set_parameter_code('PRES_01')
        poly1.set_calibration_date('11-JUN-1995 05:35:46.82')
        poly1.set_application_date('11-JUN-1995 05:35:46.82')
        poly1.set_number_coefficients(2)
        poly1.set_coefficients(['0.60000000D+01',  '0.15000001D+00'])
        print(poly1.print_object())

        poly2 = PolynomialCalHeader()
        poly2.set_parameter_code('TEMP_01')
        poly2.set_calibration_date('11-JUN-1995 05:35:46.83')
        poly2.set_application_date('11-JUN-1995 05:35:46.83')
        poly2.set_number_coefficients(2)
        poly2.set_coefficients(['0.00000000D+01',  '0.25000001D-03'])
        print(poly2.print_object())

if __name__ == "__main__":

    PolynomialCalHeader.main()