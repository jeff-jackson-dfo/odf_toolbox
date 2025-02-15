from odf_toolbox import odfutils

class PolynomialCalHeader:
    def __init__(self):
        self._parameter_code = None
        self._calibration_date = None
        self._application_date = None
        self._number_coefficients = 0
        self._coefficients = []

    def get_parameter_code(self) -> str:
        return self._parameter_code

    def set_parameter_code(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            odfutils.logger.info(f"Polynomial_Cal_Header.Parameter_Code changed from "
                                 f"{self._parameter_code} to '{value}'")
        self._parameter_code = f"'{value}'"

    def get_calibration_date(self) -> str:
        return self._calibration_date

    def set_calibration_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            odfutils.logger.info(f"Polynomial_Cal_Header.Calibration_Date changed from "
                                 f"{self._calibration_date} to '{value}'")
        self._calibration_date = f"'{value}'"

    def get_application_date(self) -> str:
        return self._application_date

    def set_application_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            odfutils.logger.info(f"Polynomial_Cal_Header.Application_Date changed from "
                                 f"{self._application_date} to '{value}'")
        self._application_date = f"'{value}'"

    def get_number_coefficients(self) -> int:
        return self._number_coefficients

    def set_number_coefficients(self, value: int, read_operation: bool = False) -> None:
        assert isinstance(value, int), \
               f"Input value is not of type int: {value}"
        if not read_operation:
            odfutils.logger.info(f"Polynomial_Cal_Header.Number_Coefficients changed from "
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
        if coefficient_number == 0 and number_coefficients == 0:
            if not read_operation:
                odfutils.logger.info(f"The following set of coefficients was added to "
                                     f"Polynomial_Cal_Header.Coefficients: {coefficient_list}")
            self._coefficients = coefficient_list
        elif coefficient_number == 0 and number_coefficients > 0:
            if not read_operation:
                odfutils.logger.info(f"The following set of coefficients was added to "
                                     f"Polynomial_Cal_Header.Coefficients: {coefficient_list}")
            self._coefficients.extend(coefficient_list)
        elif coefficient_number <= number_coefficients and number_coefficients > 0:
            if len(coefficient_list) == 1:
                if not read_operation:
                    odfutils.logger.info(f"Coefficient {coefficient_list.pop()} in "
                                         f"Polynomial_Cal_Header.Coefficients was "
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
                        coefficient_floats = [float(coefficient) for coefficient in coefficient_list]
                        self.set_coefficients(coefficient_floats, read_operation=True)
        return self

    def print_object(self) -> str:
        polynomial_header_output = "POLYNOMIAL_CAL_HEADER\n"
        polynomial_header_output += f"  PARAMETER_CODE = {odfutils.check_string(self.get_parameter_code())}\n"
        polynomial_header_output += (f"  CALIBRATION_DATE ="
                                     f"{odfutils.check_datetime(self.get_calibration_date())}\n")
        polynomial_header_output += (f"  APPLICATION_DATE = "
                                     f"{odfutils.check_datetime(self.get_application_date())}\n")
        polynomial_header_output += (f"  NUMBER_COEFFICIENTS = "
                                     f"{odfutils.check_int_value(self.get_number_coefficients())}\n")
        coefficients_list = self.get_coefficients()
        coefficients_print = ""
        for coefficient in coefficients_list:
            coefficients_print = coefficients_print + "{:.8e}".format(coefficient) + " "
        polynomial_header_output += f"  COEFFICIENTS = {coefficients_print}\n"
        return polynomial_header_output
