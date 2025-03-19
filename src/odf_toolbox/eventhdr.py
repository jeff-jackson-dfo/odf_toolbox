from odf_toolbox import BaseHeader
from odf_toolbox import odfutils

class EventHeader(BaseHeader):
    
    def __init__(self):
        super().__init__()
        self._data_type = ''
        self._event_number = ''
        self._event_qualifier1 = ''
        self._event_qualifier2 = ''
        self._creation_date = ''
        self._orig_creation_date = ''
        self._start_date_time = ''
        self._end_date_time = ''
        self._initial_latitude = None
        self._initial_longitude = None
        self._end_latitude = None
        self._end_longitude = None
        self._min_depth = None
        self._max_depth = None
        self._sampling_interval = None
        self._sounding = None
        self._depth_off_bottom = None
        self._station_name = ''
        self._set_number = ''
        self._event_comments = []

    def log_message(self, message):
        super().log_message(f"In Event Header field {message}")

    def get_data_type(self) -> str:
        return self._data_type

    def set_data_type(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'DATA_TYPE was changed from "{self._data_type}" to "{value}"')
        self._data_type = f'{value}'

    def get_event_number(self) -> str:
        return self._event_number

    def set_event_number(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'EVENT_NUMBER was changed from "{self._event_number}" to "{value}"')
        self._event_number = f'{value}'

    def get_event_qualifier1(self) -> str:
        return self._event_qualifier1

    def set_event_qualifier1(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'EVENT_QUALIFIER1 was changed from "{self._event_qualifier1}" to "{value}"')
        self._event_qualifier1 = f'{value}'

    def get_event_qualifier2(self) -> str:
        return self._event_qualifier2

    def set_event_qualifier2(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'EVENT_QUALIFIER2 was changed from "{self._event_qualifier2}" to "{value}"')
        self._event_qualifier2 = f'{value}'

    def get_creation_date(self) -> str:
        return self._creation_date

    def set_creation_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'CREATION_DATE was changed from "{self._creation_date}" to "{value}"')
        self._creation_date = f'{value}'

    def get_orig_creation_date(self) -> str:
        return self._orig_creation_date

    def set_orig_creation_date(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'ORIG_CREATION_DATE was changed from "{self._orig_creation_date}" to "{value}"')
        self._orig_creation_date = f'{value}'

    def get_start_date_time(self) -> str:
        return self._start_date_time

    def set_start_date_time(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'START_DATE_TIME was changed from "{self._start_date_time}" to "{value}"')
        self._start_date_time = f'{value}'

    def get_end_date_time(self) -> str:
        return self._end_date_time

    def set_end_date_time(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'END_DATE_TIME was changed from "{self._end_date_time}" to "{value}"')
        self._end_date_time = f'{value}'

    def get_initial_latitude(self) -> float:
        return self._initial_latitude

    def set_initial_latitude(self, value: float, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to float
            try:
                value = float(value)
            except ValueError:
                f"Input value could not be successfully converted to type float: {value}"
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f"INITIAL_LATITUDE was changed from {self._initial_latitude} to {value}")
        self._initial_latitude = value

    def get_initial_longitude(self) -> float:
        return self._initial_longitude

    def set_initial_longitude(self, value: float, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to float
            try:
                value = float(value)
            except ValueError:
                f"Input value could not be successfully converted to type float: {value}"
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f"INITIAL_LONGITUDE was changed from {self._initial_longitude} to {value}")
        self._initial_longitude = value

    def get_end_latitude(self) -> float:
        return self._end_latitude

    def set_end_latitude(self, value: float, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to float
            try:
                value = float(value)
            except ValueError:
                f"Input value could not be successfully converted to type float: {value}"
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f"END_LATITUDE was changed from {self._end_latitude} to {value}")
        self._end_latitude = value

    def get_end_longitude(self) -> float:
        return self._end_longitude

    def set_end_longitude(self, value: float, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to float
            try:
                value = float(value)
            except ValueError:
                f"Input value could not be successfully converted to type float: {value}"
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f"END_LONGITUDE was changed from {self._end_longitude} to {value}")
        self._end_longitude = value

    def get_min_depth(self) -> float:
        return self._min_depth

    def set_min_depth(self, value: float, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to float
            try:
                value = float(value)
            except ValueError:
                f"Input value could not be successfully converted to type float: {value}"
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f"MIN_DEPTH was changed from {self._min_depth} to {value}")
        self._min_depth = value

    def get_max_depth(self) -> float:
        return self._max_depth

    def set_max_depth(self, value: float, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to float
            try:
                value = float(value)
            except ValueError:
                f"Input value could not be successfully converted to type float: {value}"
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f"MAX_DEPTH was changed from {self._max_depth} to {value}")
        self._max_depth = value

    def get_sampling_interval(self) -> float:
        return self._sampling_interval

    def set_sampling_interval(self, value: float, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to float
            try:
                value = float(value)
            except ValueError:
                f"Input value could not be successfully converted to type float: {value}"
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f"SAMPLING_INTERVAL was changed from {self._sampling_interval} to {value}")
        self._sampling_interval = value

    def get_sounding(self) -> float:
        return self._sounding

    def set_sounding(self, value: float, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to float
            try:
                value = float(value)
            except ValueError:
                f"Input value could not be successfully converted to type float: {value}"
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f"SOUNDING was changed from {self._sounding} to {value}")
        self._sounding = value

    def get_depth_off_bottom(self) -> float:
        return self._depth_off_bottom

    def set_depth_off_bottom(self, value: float, read_operation: bool = False) -> None:
        if read_operation:
            # convert string to float
            try:
                value = float(value)
            except ValueError:
                f"Input value could not be successfully converted to type float: {value}"
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f"DEPTH_OFF_BOTTOM was changed from {self._depth_off_bottom} to {value}")
        self._depth_off_bottom = value

    def get_station_name(self) -> str:
        return self._station_name

    def set_station_name(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'STATION_NAME was changed from "{self._station_name}" to "{value}"')
        self._station_name = f'{value}'

    def get_set_number(self) -> str:
        return self._set_number

    def set_set_number(self, value: str, read_operation: bool = False) -> None:
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        value = value.strip("\' ")
        if not read_operation:
            self.log_message(f'SET_NUMBER was changed from "{self._set_number}" to "{value}"')
        self._set_number = f'{value}'

    def get_event_comments(self) -> list:
        return self._event_comments

    def set_event_comments(self, event_comment: str, comment_number: int = 0, read_operation: bool = False) -> None:
        assert isinstance(event_comment, str), \
               f"Input value is not of type str: {event_comment}"
        assert isinstance(comment_number, int), \
               f"Input value is not of type int: {comment_number}"
        event_comment = event_comment.strip("\'")
        number_of_comments = len(self.get_event_comments())
        if comment_number == 0 and number_of_comments >= 0:
            if not read_operation:
                self.log_message(f'The following comment was added to EVENT_COMMENTS: '
                                     f'"{event_comment}"')
            self._event_comments.append(f'{event_comment}')
        elif comment_number <= number_of_comments and number_of_comments > 0:
            if not read_operation:
                self.log_message(f'Comment {comment_number} in EVENT_COMMENTS was changed from '
                                     f'"{self._event_comments[comment_number-1]}" to "{event_comment}"')
            self._event_comments[comment_number-1] = f'{event_comment}'
        else:
            raise ValueError("The 'event_comment' number does not match the number of EVENT_COMMENTS lines.")

    def populate_object(self, event_fields: list):
        assert isinstance(event_fields, list), \
               f"Input value is not of type list: {event_fields}"
        for header_line in event_fields:
            tokens = header_line.split('=', maxsplit=1)
            event_dict = odfutils.list_to_dict(tokens)
            for key, value in event_dict.items():
                key = key.strip()
                value = value.strip()
                match key:
                    case 'DATA_TYPE':
                        self.set_data_type(value, read_operation=True)
                    case 'EVENT_NUMBER':
                        self.set_event_number(value, read_operation=True)
                    case 'EVENT_QUALIFIER1':
                        self.set_event_qualifier1(value, read_operation=True)
                    case 'EVENT_QUALIFIER2':
                        self.set_event_qualifier2(value, read_operation=True)
                    case 'CREATION_DATE':
                        self.set_creation_date(value, read_operation=True)
                    case 'ORIG_CREATION_DATE':
                        self.set_orig_creation_date(value, read_operation=True)
                    case 'START_DATE_TIME':
                        self.set_start_date_time(value, read_operation=True)
                    case 'END_DATE_TIME':
                        self.set_end_date_time(value, read_operation=True)
                    case 'INITIAL_LATITUDE':
                        self.set_initial_latitude(value, read_operation=True)
                    case 'INITIAL_LONGITUDE':
                        self.set_initial_longitude(value, read_operation=True)
                    case 'END_LATITUDE':
                        self.set_end_latitude(value, read_operation=True)
                    case 'END_LONGITUDE':
                        self.set_end_longitude(value, read_operation=True)
                    case 'MIN_DEPTH':
                        self.set_min_depth(value, read_operation=True)
                    case 'MAX_DEPTH':
                        self.set_max_depth(value, read_operation=True)
                    case 'SAMPLING_INTERVAL':
                        self.set_sampling_interval(value, read_operation=True)
                    case 'SOUNDING':
                        self.set_sounding(value, read_operation=True)
                    case 'DEPTH_OFF_BOTTOM':
                        self.set_depth_off_bottom(value, read_operation=True)
                    case 'STATION_NAME':
                        self.set_station_name(value, read_operation=True)
                    case 'SET_NUMBER':
                        self.set_set_number(value, read_operation=True)
                    case 'EVENT_COMMENTS':
                        self.set_event_comments(value, read_operation=True)
        return self

    def print_object(self) -> str:
        event_header_output = "EVENT_HEADER\n"
        event_header_output += f"  DATA_TYPE = '{self.get_data_type()}'\n"
        event_header_output += f"  EVENT_NUMBER = '{self.get_event_number()}'\n"
        event_header_output += f"  EVENT_QUALIFIER1 = '{self.get_event_qualifier1()}'\n"
        event_header_output += f"  EVENT_QUALIFIER2 = '{self.get_event_qualifier2()}'\n"
        event_header_output += f"  CREATION_DATE = '{odfutils.check_datetime(self.get_creation_date())}'\n"
        event_header_output += f"  ORIG_CREATION_DATE = '{odfutils.check_datetime(self.get_orig_creation_date())}'\n"
        event_header_output += f"  START_DATE_TIME = '{odfutils.check_datetime(self.get_start_date_time())}'\n"
        event_header_output += f"  END_DATE_TIME = '{odfutils.check_datetime(self.get_end_date_time())}'\n"
        event_header_output += (f"  INITIAL_LATITUDE = "
                                f"{odfutils.check_long(self.get_initial_latitude()):.6f}\n")
        event_header_output += (f"  INITIAL_LONGITUDE = "
                                f"{odfutils.check_long(self.get_initial_longitude()):.6f}\n")
        event_header_output += f"  END_LATITUDE = {odfutils.check_float(self.get_end_latitude()):.6f}\n"
        event_header_output += f"  END_LONGITUDE = {odfutils.check_long(self.get_end_longitude()):.6f}\n"
        event_header_output += f"  MIN_DEPTH = {odfutils.check_float(self.get_min_depth()):.2f}\n"
        event_header_output += f"  MAX_DEPTH = {odfutils.check_float(self.get_max_depth()):.2f}\n"
        event_header_output += (f"  SAMPLING_INTERVAL = "
                                f"{odfutils.check_float(self.get_sampling_interval()):.2f}\n")
        event_header_output += f"  SOUNDING = {odfutils.check_float(self.get_sounding()):.2f}\n"
        event_header_output += f"  DEPTH_OFF_BOTTOM = {odfutils.check_float(self.get_depth_off_bottom()):.2f}\n"
        event_header_output += f"  STATION_NAME = '{self.get_station_name()}'\n"
        event_header_output += f"  SET_NUMBER = '{self.get_set_number()}'\n"
        if self.get_event_comments():
            for event_comment in self.get_event_comments():
                event_header_output += f"  EVENT_COMMENTS = '{event_comment}'\n"
        else:
            event_header_output += "  EVENT_COMMENTS = ''\n"
        return event_header_output

    def main():
        event = EventHeader()
        event.set_creation_date('2021-03-25T00:00:00')
        event.set_data_type('CTD')
        event.set_event_number('001')
        event.set_event_qualifier1('123456')
        event.set_event_qualifier2('DN')
        event.set_creation_date('2025-03-14T08:55:00')
        event.set_orig_creation_date('2024-10-25T12:20:00')
        event.set_start_date_time('2017-07-03T19:12:00')
        event.set_end_date_time('2017-07-03T20:05:00')
        event.set_initial_latitude(33.123456)
        event.set_initial_longitude(-118.123456)
        event.set_end_latitude(33.123456)
        event.set_end_longitude(-118.123456)
        event.set_min_depth(0.0)
        event.set_max_depth(100.0)
        event.set_sampling_interval(1.0)
        event.set_sounding(110.0)
        event.set_depth_off_bottom(10.0)
        event.set_station_name('Station Name')
        event.set_set_number('001')
        event.set_event_comments('Comment 1')
        print(event.print_object())


if __name__ == "__main__":

    EventHeader.main()