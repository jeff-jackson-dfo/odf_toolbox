from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel
from icecream import ic
class QualityHeader(BaseModel, BaseHeader):
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

    def __init__(self, 
                 quality_date: str = '',
                 quality_tests: list = [],
                 quality_comments: list = []
                 ):
        super().__init__()
        self.quality_date = quality_date
        self.quality_tests = quality_tests
        self.quality_comments = quality_comments

    def log_message(self, field: str, old_value: str, new_value: str) -> NoReturn:
        message = f"In Quality Header field {field.upper()} was changed from '{old_value}' to '{new_value}'"
        super().log_message(message)

    @property
    def quality_date(self):
        return self._quality_date

    @quality_date.setter
    def quality_date(self, value: str) -> NoReturn:
        self._quality_date = value.upper()

    @property
    def quality_tests(self):
        return self._quality_tests

    @quality_tests.setter
    def quality_tests(self, quality_tests: list) -> NoReturn:
        self._quality_tests = quality_tests

    def set_quality_test(self, quality_test: str, test_number: int = 0) -> NoReturn:
        number_of_tests = len(self.quality_tests)
        if test_number == 0 and number_of_tests >= 0:
            self._quality_tests.append(quality_test)
        elif test_number <= number_of_tests and number_of_tests > 0:
            self._quality_tests[test_number] = quality_test
        else:
            raise ValueError("The 'quality_test' number does not match the number of QUALITY_TESTS lines.")

    @property
    def quality_comments(self):
        return self._quality_comments

    @quality_comments.setter
    def quality_comments(self, quality_comments: list) -> NoReturn:
        self._quality_comments = quality_comments

    def set_quality_comment(self, quality_comment: str, comment_number: int = 0) -> NoReturn:
        number_of_comments = len(self.quality_comments)
        if comment_number == 0 and number_of_comments >= 0:
            self._quality_comments.append(quality_comment)
        elif comment_number <= number_of_comments and number_of_comments > 0:
            self._quality_comments[comment_number] = quality_comment
        else:
            raise ValueError("The 'quality_comment' number does not match the number of QUALITY_COMMENTS lines.")

    def populate_object(self, quality_fields: list):
        for header_line in quality_fields:
            tokens = header_line.split('=', maxsplit=1)
            quality_dict = odfutils.list_to_dict(tokens)
            for key, value in quality_dict.items():
                key = key.strip("\' ")
                value = value.strip("\' ")
                match key:
                    case 'QUALITY_DATE':
                        self.quality_date = value
                    case 'QUALITY_TESTS':
                        self.set_quality_test(value)
                    case 'QUALITY_COMMENTS':
                        self.set_quality_comment(value)

    def print_object(self) -> str:
        quality_header_output = "QUALITY_HEADER\n"
        quality_header_output += f"  QUALITY_DATE = '{odfutils.check_string(self.quality_date)}'\n"
        for quality_test in self.quality_tests:
            quality_header_output += f"  QUALITY_TESTS = '{quality_test}'\n"
        for quality_comment in self.quality_comments:
            quality_header_output += f"  QUALITY_COMMENTS = '{quality_comment}'\n"
        return quality_header_output

    def main():

        quality_header = QualityHeader()
        sytm = '01-JUL-2017 10:45:19.00'
        quality_header.quality_date = sytm
        quality_header.set_quality_test('Test 1')
        quality_header.set_quality_test('Test 2')
        quality_header.quality_comments = ['Comment 1', 'Comment 2']
        print(quality_header.print_object())

if __name__ == '__main__':
    QualityHeader.main()
