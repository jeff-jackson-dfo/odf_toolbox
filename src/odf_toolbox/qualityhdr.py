from odf_toolbox.basehdr import BaseHeader
from odf_toolbox import odfutils

class QualityHeader(BaseHeader):
    """
    A class to represent a Quality Header in an ODF object.

    Attributes:
    -----------
    _quality_date : string
        the date time when the Quality Header was added to the ODF object
    _quality_tests : list of strings
        list of quality control tests run on the ODF object's data
    _quality_comments : list of strings
        list of comments regarding the quality control carried out on the ODF object's data

    Methods:
    -------
    __init__ :
        initialize a QualityHeader class object
    get_quality_date : string
    set_quality_date : None
    get_quality_tests : list of strings
    set_quality_tests : None
    add_quality_tests : None
    get_quality_comments : list of strings
    set_quality_comments : None
    add_quality_comments : None

    """

    def __init__(self):
        super().__init__()
        self._quality_date = None
        self._quality_tests = []
        self._quality_comments = []

    def log_message(self, message):
        super().log_message(f"QUALITY_HEADER: {message}")

    def get_quality_date(self):
        return self._quality_date

    def set_quality_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        if not read_operation:
            self.log_message(f"QUALITY_DATE was changed from {self._quality_date} to '{value}'")
        self._quality_date = value

    def get_quality_tests(self):
        return self._quality_tests

    def set_quality_tests(self, quality_test: str, test_number: int = 0, read_operation: bool = False) -> None:
        assert isinstance(quality_test, str), \
               f"Input value is not of type str: {quality_test}"
        assert isinstance(test_number, int), \
               f"Input value is not of type int: {test_number}"
        number_of_tests = len(self.get_quality_tests())
        if test_number == 0 and number_of_tests >= 0:
            if not read_operation:
                self.log_message(f"The following quality test was added to QUALITY_TESTS: "
                                     f"'{quality_test}'")
            self._quality_tests.append(quality_test)
        elif test_number <= number_of_tests and number_of_tests > 0:
            if not read_operation:
                self.log_message(f"Quality Test {test_number} in QUALITY_TESTS was changed from "
                                     f"{self._quality_tests[test_number-1]} to '{quality_test}'")
            self._quality_tests[test_number] = quality_test
        else:
            raise ValueError("The 'quality_test' number does not match the number of QUALITY_TESTS lines.")

    def get_quality_comments(self):
        return self._quality_comments

    def set_quality_comments(self, quality_comment: str, comment_number: int = 0, read_operation: bool = False) -> None:
        assert isinstance(quality_comment, str), \
               f"Input value is not of type str: {quality_comment}"
        assert isinstance(comment_number, int), \
               f"Input value is not of type int: {comment_number}"
        number_of_comments = len(self.get_quality_comments())
        if comment_number == 0 and number_of_comments >= 0:
            if not read_operation:
                self.log_message(f"The following quality comment was added to QUALITY_COMMENTS: "
                                     f"'{quality_comment}'")
            self._quality_comments.append(quality_comment)
        elif comment_number <= number_of_comments and number_of_comments > 0:
            if not read_operation:
                self.log_message(f"Quality Comment {comment_number} in QUALITY_COMMENTS was "
                                     f"changed from {self._quality_comments[comment_number-1]} to '{quality_comment}'")
            self._quality_comments[comment_number] = quality_comment
        else:
            raise ValueError("The 'quality_comment' number does not match the number of QUALITY_COMMENTS lines.")

    def populate_object(self, quality_fields: list):
        assert isinstance(quality_fields, list), \
               f"Input value is not of type list: {quality_fields}"
        for header_line in quality_fields:
            tokens = header_line.split('=', maxsplit=1)
            quality_dict = odfutils.list_to_dict(tokens)
            for key, value in quality_dict.items():
                key = key.strip()
                value = value.strip()
                match key:
                    case 'QUALITY_DATE':
                        self.set_quality_date(value, read_operation=True)
                    case 'QUALITY_TESTS':
                        self.set_quality_tests(value, read_operation=True)
                    case 'QUALITY_COMMENTS':
                        self.set_quality_comments(value, read_operation=True)

    def print_object(self) -> str:
        quality_header_output = "QUALITY_HEADER\n"
        quality_header_output += f"  QUALITY_DATE = {odfutils.check_string(self.get_quality_date())}\n"
        for quality_test in self.get_quality_tests():
            quality_header_output += f"  QUALITY_TESTS = {quality_test}\n"
        for quality_comment in self.get_quality_comments():
            quality_header_output += f"  QUALITY_COMMENTS = {quality_comment}\n"
        return quality_header_output
