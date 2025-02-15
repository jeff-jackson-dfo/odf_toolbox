from odf_toolbox import odfutils

class GeneralCalHeader:
    def __init__(self):
        self._parameter_code = "''"
        self._calibration_type = "''"
        self._calibration_date = "''"
        self._application_date = "''"
        self._number_coefficients = None
        self._coefficients = []
        self._calibration_equation = "''"
        self._calibration_comments = []

    def get_parameter_code(self) -> str:
        return self._parameter_code

    def set_parameter_code(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            odfutils.logger.info(f"General_Cal_Header.Parameter_Code changed from "
                                 f"{self._parameter_code} to '{value}'")
        self._parameter_code = f"'{value}'"

    def get_calibration_type(self) -> str:
        return self._calibration_type

    def set_calibration_type(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            odfutils.logger.info(f"General_Cal_Header.Calibration_Type changed from "
                                 f"{self._calibration_type} to '{value}'")
        self._calibration_type = f"'{value}'"

    def get_calibration_date(self) -> str:
        return self._calibration_date

    def set_calibration_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            odfutils.logger.info(f"General_Cal_Header.Calibration_Date changed from "
                                 f"{self._calibration_date} to '{value}'")
        self._calibration_date = f"'{value}'"

    def get_application_date(self) -> str:
        return self._application_date

    def set_application_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            odfutils.logger.info(f"General_Cal_Header.Application_Date changed from "
                                 f"{self._application_date} to '{value}'")
        self._application_date = f"'{value}'"

    def get_number_coefficients(self) -> int:
        return self._number_coefficients

    def set_number_coefficients(self, value: int, read_operation: bool = False) -> None:
        assert isinstance(value, int), \
               f"Input value is not of type int: {value}"
        if not read_operation:
            odfutils.logger.info(f"General_Cal_Header.Number_Coefficients changed from "
                                 f"{self._number_coefficients} to '{value}'")
        self._number_coefficients = value

    def get_coefficients(self) -> list:
        return self._coefficients

    def set_coefficients(self, general_coefficient_list: list, general_coefficient_number: int = 0,
                         read_operation: bool = False) -> None:
        assert isinstance(general_coefficient_list, list), \
               f"Input value is not of type list: {general_coefficient_list}"
        assert isinstance(general_coefficient_number, int), \
               f"Input value is not of type int: {general_coefficient_number}"
        number_of_general_coefficients = self.get_number_coefficients()
        if general_coefficient_number == 0:
            if number_of_general_coefficients == 0:
                if not read_operation:
                    odfutils.logger.info(f"The following set of coefficients was added to "
                                         f"General_Cal_Header.Coefficients: {general_coefficient_list}")
                self._coefficients = general_coefficient_list
            elif number_of_general_coefficients > 0:
                if not read_operation:
                    odfutils.logger.info(f"The following set of coefficients was added to "
                                         f"General_Cal_Header.Coefficients: {general_coefficient_list}")
                self._coefficients.extend(general_coefficient_list)
            elif general_coefficient_number <= number_of_general_coefficients and number_of_general_coefficients > 0:
                if len(general_coefficient_list) == 1:
                    if not read_operation:
                        odfutils.logger.info(f"Coefficient {general_coefficient_list.pop()} in "
                                             f"General_Cal_Header.Coefficients was "
                                             f"changed from {self._coefficients[general_coefficient_number - 1]} "
                                             f"to {general_coefficient_list.pop()}")
                    self._coefficients[general_coefficient_number] = general_coefficient_list.pop()
            else:
                raise ValueError("The 'coefficient_number' does not match the number of COEFFICIENTS.")

    def get_calibration_equation(self) -> str:
        return self._calibration_equation

    def set_calibration_equation(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            odfutils.logger.info(f"General_Cal_Header.Parameter_Code changed from "
                                 f"{self._parameter_code} to '{value}'")
        self._calibration_equation = f"'{value}'"

    def get_calibration_comments(self) -> list:
        return self._calibration_comments

    def set_calibration_comments(self, calibration_comment: str, comment_number: int = 0,
                                 read_operation: bool = False) -> None:
        assert isinstance(calibration_comment, str), \
               f"Input value is not of type str: {calibration_comment}"
        assert isinstance(comment_number, int), \
               f"Input value is not of type int: {comment_number}"
        calibration_comment = calibration_comment.strip("\'")
        number_of_comments = len(self.get_calibration_comments())
        if comment_number == 0 and number_of_comments >= 0:
            if not read_operation:
                odfutils.logger.info(f"The following comment was added to General_Cal_Header.Calibration_Comments: "
                                     f"'{calibration_comment}'")
            self._calibration_comments.append(f"'{calibration_comment}'")
        elif comment_number <= number_of_comments and number_of_comments > 0:
            if not read_operation:
                odfutils.logger.info(f"Comment {comment_number} in General_Cal_Header.Calibration_Comments was "
                                     f"changed from {self._calibration_comments[comment_number-1]} to "
                                     f"'{calibration_comment}'")
            self._calibration_comments[comment_number] = f"'{calibration_comment}'"
        else:
            raise ValueError("The 'calibration_comment' number does not match the number of "
                             "CALIBRATION_COMMENTS lines.")

    def populate_object(self, general_cal_fields: list):
        for header_line in general_cal_fields:
            tokens = header_line.split('=', maxsplit=1)
            general_dict = odfutils.list_to_dict(tokens)
            for key, value in general_dict.items():
                key = key.strip()
                value = value.strip()
                match key:
                    case 'PARAMETER_CODE':
                        self.set_parameter_code(value, read_operation=True)
                    case 'CALIBRATION_TYPE':
                        self.set_calibration_type(value, read_operation=True)
                    case 'CALIBRATION_DATE':
                        self.set_calibration_date(value, read_operation=True)
                    case 'APPLICATION_DATE':
                        self.set_application_date(value, read_operation=True)
                    case 'NUMBER_OF_COEFFICIENTS':
                        self.set_number_coefficients(int(value), read_operation=True)
                    case 'COEFFICIENTS':
                        coefficient_list = value.split()
                        coefficient_floats = [float(coefficient) for coefficient in coefficient_list]
                        self.set_coefficients(coefficient_floats, read_operation=True)
                    case 'CALIBRATION_EQUATION':
                        self.set_calibration_equation(value, read_operation=True)
                    case 'CALIBRATION_COMMENTS':
                        self.set_calibration_comments(value, read_operation=True)
        return self

    # noinspection DuplicatedCode
    def print_object(self) -> str:
        general_header_output = "GENERAL_CAL_HEADER\n"
        general_header_output += f"  PARAMETER_CODE = {odfutils.check_string(self.get_parameter_code())}\n"
        general_header_output += (f"  CALIBRATION_TYPE = "
                                  f"{odfutils.check_string(self.get_calibration_type())}\n")
        general_header_output += (f"  CALIBRATION_DATE = "
                                  f"{odfutils.check_datetime(self.get_calibration_date())}\n")
        general_header_output += (f"  APPLICATION_DATE = "
                                  f"{odfutils.check_datetime(self.get_application_date())}\n")
        general_header_output += (f"  NUMBER_OF_COEFFICIENTS = "
                                  f"{odfutils.check_int_value(self.get_number_coefficients())}\n")
        coefficients_list = self.get_coefficients()
        coefficients_print = ""
        for coefficient in coefficients_list:
            coefficients_print = coefficients_print + "{:.8e}".format(coefficient) + " "
        general_header_output += f"  COEFFICIENTS = {coefficients_print}\n"
        general_header_output += (f"  CALIBRATION_EQUATION = "
                                  f"{odfutils.check_string(self.get_calibration_equation())}\n")
        for general_comment in self.get_calibration_comments():
            general_header_output += f"  CALIBRATION_COMMENTS = {general_comment}\n"
        return general_header_output
