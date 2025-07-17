from odf_toolbox.basehdr import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class EventHeader(BaseModel, BaseHeader):
    """ A class to represent an Event Header in an ODF object. """
    def __init__(self, 
                 data_type: str = None, 
                 event_number: str = None, 
                 event_qualifier1: str = None, 
                 event_qualifier2: str = None, 
                 creation_date: str = None, 
                 orig_creation_date: str = None,
                 start_date_time: str = None, 
                 end_date_time: str = None, 
                 initial_latitude: float = None, 
                 initial_longitude: float = None, 
                 end_latitude: float = None, 
                 end_longitude: float = None,
                 min_depth: float = None, 
                 max_depth: float = None, 
                 sampling_interval: float = None, 
                 sounding: float = None, 
                 depth_off_bottom: float = None, 
                 station_name: str = None, 
                 set_number: str = None, 
                 event_comments: list = None
                 ) -> NoReturn:
        super().__init__()
        self.data_type = data_type if data_type is not None else ''
        self.event_number = event_number if event_number is not None else ''
        self.event_qualifier1 = event_qualifier1 if event_qualifier1 is not None else ''
        self.event_qualifier2 = event_qualifier2 if event_qualifier2 is not None else ''
        self.creation_date = creation_date if creation_date is not None else BaseHeader.SYTM_NULL_VALUE
        self.orig_creation_date = orig_creation_date if orig_creation_date is not None else BaseHeader.SYTM_NULL_VALUE
        self.start_date_time = start_date_time if start_date_time is not None else BaseHeader.SYTM_NULL_VALUE
        self.end_date_time = end_date_time if end_date_time is not None else BaseHeader.SYTM_NULL_VALUE
        self.initial_latitude = initial_latitude if initial_latitude is not None else BaseHeader.NULL_VALUE
        self.initial_longitude = initial_longitude if initial_longitude is not None else BaseHeader.NULL_VALUE
        self.end_latitude = end_latitude if end_latitude is not None else BaseHeader.NULL_VALUE
        self.end_longitude = end_longitude if end_longitude is not None else BaseHeader.NULL_VALUE
        self.min_depth = min_depth if min_depth is not None else BaseHeader.NULL_VALUE
        self.max_depth = max_depth if max_depth is not None else BaseHeader.NULL_VALUE
        self.sampling_interval = sampling_interval if sampling_interval is not None else BaseHeader.NULL_VALUE
        self.sounding = sounding if sounding is not None else BaseHeader.NULL_VALUE
        self.depth_off_bottom = depth_off_bottom if depth_off_bottom is not None else BaseHeader.NULL_VALUE
        self.station_name = station_name if station_name is not None else ''
        self.set_number = set_number if set_number is not None else ''
        self.event_comments = event_comments if event_comments is not None else []
        
    def log_event_message(self, field: str, old_value: any, new_value: any) -> NoReturn:
        assert isinstance(field, str), "Input argument 'field' must be a string."
        if field.upper() == 'EVENT_COMMENTS':
            print("Use method 'update_event_comments' to modify EVENT_COMMENTS.")
            return
        if field.upper() == 'DATA_TYPE' or \
           field.upper() == 'EVENT_NUMBER' or \
           field.upper() == 'EVENT_QUALIFIER1' or \
           field.upper() == 'EVENT_QUALIFIER2' or \
           field.upper() == 'CREATION_DATE' or \
           field.upper() == 'ORIG_CREATION_DATE' or \
           field.upper() == 'START_DATE_TIME' or \
           field.upper() == 'END_DATE_TIME' or \
           field.upper() == 'STATION_NAME' or \
           field.upper() == 'SET_NUMBER':
            # old_value = "''"'
           message = f'In Event Header field {field.upper()} was changed from "{old_value}" to "{new_value}"'
        else:    
            message = f'In Event Header field {field.upper()} was changed from {old_value} to {new_value}'
        super().log_message(message)

    @property
    def data_type(self) -> str:
        return self._data_type

    @data_type.setter
    def data_type(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("\' ")
        self._data_type = value

    @property
    def event_number(self) -> str:
        return self._event_number

    @event_number.setter
    def event_number(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("\' ")
        self._event_number = value

    @property
    def event_qualifier1(self) -> str:
        return self._event_qualifier1

    @event_qualifier1.setter
    def event_qualifier1(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("\' ")
        self._event_qualifier1 = value

    @property
    def event_qualifier2(self) -> str:
        return self._event_qualifier2

    @event_qualifier2.setter
    def event_qualifier2(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("\' ")
        self._event_qualifier2 = value

    @property
    def creation_date(self) -> str:
        return self._creation_date

    @creation_date.setter
    def creation_date(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = odfutils.check_datetime(value)
        value = value.strip("\' ")
        self._creation_date = value.upper()

    @property
    def orig_creation_date(self) -> str:
        return self._orig_creation_date

    @orig_creation_date.setter
    def orig_creation_date(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("\' ")
        value = odfutils.check_datetime(value)
        self._orig_creation_date = value.upper()

    @property
    def start_date_time(self) -> str:
        return self._start_date_time

    @start_date_time.setter
    def start_date_time(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("\' ")
        value = odfutils.check_datetime(value)
        self._start_date_time = value.upper()

    @property
    def end_date_time(self) -> str:
        return self._end_date_time

    @end_date_time.setter
    def end_date_time(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        value = value.strip("\' ")
        value = odfutils.check_datetime(value)
        self._end_date_time = value.upper()

    @property
    def initial_latitude(self) -> float:
        return self._initial_latitude

    @initial_latitude.setter
    def initial_latitude(self, value: float) -> NoReturn:
        assert isinstance(value, float), "Input argument 'value' must be a float."
        self._initial_latitude = value

    @property
    def initial_longitude(self) -> float:
        return self._initial_longitude

    @initial_longitude.setter
    def initial_longitude(self, value: float) -> NoReturn:
        assert isinstance(value, float), "Input argument 'value' must be a float."
        self._initial_longitude = value

    @property
    def end_latitude(self) -> float:
        return self._end_latitude

    @end_latitude.setter
    def end_latitude(self, value: float) -> NoReturn:
        assert isinstance(value, float), "Input argument 'value' must be a float."
        self._end_latitude = value

    @property
    def end_longitude(self) -> float:
        return self._end_longitude

    @end_longitude.setter
    def end_longitude(self, value: float) -> NoReturn:
        assert isinstance(value, float), "Input argument 'value' must be a float."
        self._end_longitude = value

    @property
    def min_depth(self) -> float:
        return self._min_depth

    @min_depth.setter
    def min_depth(self, value: float) -> NoReturn:
        assert isinstance(value, float), "Input argument 'value' must be a float."
        self._min_depth = value

    @property
    def max_depth(self) -> float:
        return self._max_depth

    @max_depth.setter
    def max_depth(self, value: float) -> NoReturn:
        assert isinstance(value, float), "Input argument 'value' must be a float."
        self._max_depth = value

    @property
    def sampling_interval(self) -> float:
        return self._sampling_interval

    @sampling_interval.setter
    def sampling_interval(self, value: float) -> NoReturn:
        assert isinstance(value, float), "Input argument 'value' must be a float."
        self._sampling_interval = value

    @property
    def sounding(self) -> float:
        return self._sounding

    @sounding.setter
    def sounding(self, value: float) -> NoReturn:
        assert isinstance(value, float), "Input argument 'value' must be a float."
        self._sounding = value

    @property
    def depth_off_bottom(self) -> float:
        return self._depth_off_bottom

    @depth_off_bottom.setter
    def depth_off_bottom(self, value: float) -> NoReturn:
        assert isinstance(value, float), "Input argument 'value' must be a float."
        self._depth_off_bottom = value

    @property
    def station_name(self) -> str:
        return self._station_name

    @station_name.setter
    def station_name(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        self._station_name = f'{value}'

    @property
    def set_number(self) -> str:
        return self._set_number

    @set_number.setter
    def set_number(self, value: str) -> NoReturn:
        assert isinstance(value, str), "Input argument 'value' must be a string."
        self._set_number = f'{value}'

    @property
    def event_comments(self) -> list:
        return self._event_comments

    @event_comments.setter
    def event_comments(self, value: list) -> NoReturn:
        assert isinstance(value, list), "Input argument 'value' must be a list."
        for comment in value:
            assert isinstance(comment, str), "Input argument 'value' must be a list of strings."
        self._event_comments = value
    
    def set_event_comment(self, event_comment: str, comment_number: int = 0) -> None:
        assert isinstance(event_comment, str), "Input argument 'event_comment' must be a string."
        assert isinstance(comment_number, int), "Input argument 'comment_number' must be a integer."
        event_comment = event_comment.strip("\' ")
        number_of_comments = len(self.event_comments)
        if comment_number == 0:
            self._event_comments.append(event_comment)
        elif comment_number <= number_of_comments and number_of_comments > 0:
            self._event_comments[comment_number - 1] = event_comment

    def populate_object(self, event_fields: list):
        assert isinstance(event_fields, list), "Input argument 'event_fields' must be a list."
        for header_line in event_fields:
            tokens = header_line.split('=', maxsplit=1)
            event_dict = odfutils.list_to_dict(tokens)
            for key, value in event_dict.items():
                key = key.strip()
                if str(value):
                    value = value.strip("' ")
                match key:
                    case 'DATA_TYPE':
                        self.data_type = value
                    case 'EVENT_NUMBER':
                        self.event_number = value
                    case 'EVENT_QUALIFIER1':
                        self.event_qualifier1 = value
                    case 'EVENT_QUALIFIER2':
                        self.event_qualifier2 = value
                    case 'CREATION_DATE':
                        self.creation_date = value
                    case 'ORIG_CREATION_DATE':
                        self.orig_creation_date = value
                    case 'START_DATE_TIME':
                        self.start_date_time = value
                    case 'END_DATE_TIME':
                        self.end_date_time = value
                    case 'INITIAL_LATITUDE':
                        self.initial_latitude = float(value)
                    case 'INITIAL_LONGITUDE':
                        self.initial_longitude = float(value)
                    case 'END_LATITUDE':
                        self.end_latitude = float(value)
                    case 'END_LONGITUDE':
                        self.end_longitude = float(value)
                    case 'MIN_DEPTH':
                        self.min_depth = float(value)
                    case 'MAX_DEPTH':
                        self.max_depth = float(value)
                    case 'SAMPLING_INTERVAL':
                        self.sampling_interval = float(value)
                    case 'SOUNDING':
                        self.sounding = float(value)
                    case 'DEPTH_OFF_BOTTOM':
                        self.depth_off_bottom = float(value)
                    case 'STATION_NAME':
                        self.station_name = value
                    case 'SET_NUMBER':
                        self.set_number = value
                    case 'EVENT_COMMENTS':
                        if type(value) is str:
                            self._event_comments = [value]
                        elif type(value) is list:
                            self._event_comments = value
                        else:
                            print('event_header.event_comments is not a string or list.')
        return self

    def print_object(self) -> str:
        event_header_output = "EVENT_HEADER\n"
        event_header_output += f"  DATA_TYPE = '{self.data_type}'\n"
        event_header_output += f"  EVENT_NUMBER = '{self.event_number}'\n"
        event_header_output += f"  EVENT_QUALIFIER1 = '{self.event_qualifier1}'\n"
        event_header_output += f"  EVENT_QUALIFIER2 = '{self.event_qualifier2}'\n"
        event_header_output += f"  CREATION_DATE = '{self.creation_date}'\n"
        event_header_output += f"  ORIG_CREATION_DATE = '{self.orig_creation_date}'\n"
        event_header_output += f"  START_DATE_TIME = '{self.start_date_time}'\n"
        event_header_output += f"  END_DATE_TIME = '{self.end_date_time}'\n"
        if self.initial_latitude == BaseHeader.NULL_VALUE:
            event_header_output += f"  INITIAL_LATITUDE = {self.initial_latitude}\n"
        else:
            event_header_output += f"  INITIAL_LATITUDE = {self.initial_latitude:.6f}\n"
        if self.initial_longitude == BaseHeader.NULL_VALUE:
            event_header_output += f"  INITIAL_LONGITUDE = {self.initial_longitude}\n"
        else:
            event_header_output += f"  INITIAL_LONGITUDE = {self.initial_longitude:.6f}\n"
        if self.end_latitude == BaseHeader.NULL_VALUE:
            event_header_output += f"  END_LATITUDE = {self.end_latitude}\n"
        else:
            event_header_output += f"  END_LATITUDE = {self.end_latitude:.6f}\n"
        if self.end_longitude == BaseHeader.NULL_VALUE:
            event_header_output += f"  END_LONGITUDE = {self.end_longitude}\n"
        else:
            event_header_output += f"  END_LONGITUDE = {self.end_longitude:.6f}\n"
        if self.min_depth == BaseHeader.NULL_VALUE:
            event_header_output += f"  MIN_DEPTH = {self.min_depth}\n"
        else:
            event_header_output += f"  MIN_DEPTH = {self.min_depth:.2f}\n"
        if self.max_depth == BaseHeader.NULL_VALUE:
            event_header_output += f"  MAX_DEPTH = {self.max_depth}\n"
        else:
            event_header_output += f"  MAX_DEPTH = {self.max_depth:.2f}\n"
        event_header_output += f"  SAMPLING_INTERVAL = {self.sampling_interval}\n"
        if self.sounding == BaseHeader.NULL_VALUE:
            event_header_output += f"  SOUNDING = {self.sounding}\n"
        else:
            event_header_output += f"  SOUNDING = {self.sounding:.2f}\n"
        if self.depth_off_bottom == BaseHeader.NULL_VALUE:
            event_header_output += f"  DEPTH_OFF_BOTTOM = {self.depth_off_bottom}\n"
        else:
            event_header_output += f"  DEPTH_OFF_BOTTOM = {self.depth_off_bottom:.2f}\n"
        event_header_output += f"  STATION_NAME = '{self.station_name}'\n"
        event_header_output += f"  SET_NUMBER = '{self.set_number}'\n"
        if self.event_comments:
            for event_comment in self.event_comments:
                event_header_output += f"  EVENT_COMMENTS = '{event_comment}'\n"
        else:
            event_header_output += "  EVENT_COMMENTS = ''\n"
        return event_header_output

def main():
    print()

    event = EventHeader()
    print(event.print_object())
    event.data_type = 'CTD'
    event.event_number = '001'
    event.event_qualifier1 = '123456'
    event.event_qualifier2 = 'DN'
    event.creation_date = '14-Mar-2025 08:55:00.00'
    event.orig_creation_date = '25-OCT-2024 12:20:00.00'
    event.start_date_time = '03-jul-2017 19:12:00.00'
    event.end_date_time = '03-Jul-2017 20:05:00.00'
    event.initial_latitude = 33.123456
    event.initial_longitude = -118.123456
    event.end_latitude = 33.123456
    event.end_longitude = -118.123456
    event.min_depth = 0.0
    event.max_depth = 100.0
    event.sampling_interval = 1.0
    event.sounding = 110.0
    event.depth_off_bottom = 10.0
    event.log_event_message('station_name', event.station_name, 'STN_01')
    event.station_name = 'STN_01'
    event.set_number = '001'
    event.set_event_comment('Good cast!')
    print(event.print_object())
    for log_entry in BaseHeader.shared_log_list:
        print(log_entry)
    print()

if __name__ == "__main__":
    main()