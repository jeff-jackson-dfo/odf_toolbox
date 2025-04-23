from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class EventHeader(BaseModel, BaseHeader):
    """
    A class to represent an Event Header in an ODF object.
    """    
    def __init__(self, 
                 data_type: str = '', 
                 event_number: str = '', 
                 event_qualifier1: str = '', 
                 event_qualifier2: str = '', 
                 creation_date: str = BaseHeader.sytm_null_value, 
                 orig_creation_date: str = BaseHeader.sytm_null_value,
                 start_date_time: str = BaseHeader.sytm_null_value, 
                 end_date_time: str = BaseHeader.sytm_null_value, 
                 initial_latitude: float = BaseHeader.null_value, 
                 initial_longitude: float = BaseHeader.null_value, 
                 end_latitude: float = BaseHeader.null_value, 
                 end_longitude: float = BaseHeader.null_value,
                 min_depth: float = BaseHeader.null_value, 
                 max_depth: float = BaseHeader.null_value, 
                 sampling_interval: float = BaseHeader.null_value, 
                 sounding: float = BaseHeader.null_value, 
                 depth_off_bottom: float = BaseHeader.null_value, 
                 station_name: str = '', 
                 set_number: str = '', 
                 event_comments: list = []
                 ) -> NoReturn:
        super().__init__()
        self.data_type = data_type
        self.event_number = event_number
        self.event_qualifier1 = event_qualifier1
        self.event_qualifier2 = event_qualifier2
        self.creation_date = creation_date
        self.orig_creation_date = orig_creation_date
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.initial_latitude = initial_latitude
        self.initial_longitude = initial_longitude
        self.end_latitude = end_latitude
        self.end_longitude = end_longitude
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.sampling_interval = sampling_interval
        self.sounding = sounding
        self.depth_off_bottom = depth_off_bottom
        self.station_name = station_name
        self.set_number = set_number
        self.event_comments = event_comments
        
    def log_message(self, field: str, old_value: any, new_value: any) -> NoReturn:
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
            old_value = "''"
            message = f"In Event Header field {field.upper()} was changed from {old_value} to '{new_value}'"
        else:    
            message = f"In Event Header field {field.upper()} was changed from {old_value} to {new_value}"
        super().log_message(message)

    @property
    def data_type(self) -> str:
        return self._data_type

    @data_type.setter
    def data_type(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._data_type = value

    @property
    def event_number(self) -> str:
        return self._event_number

    @event_number.setter
    def event_number(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._event_number = value

    @property
    def event_qualifier1(self) -> str:
        return self._event_qualifier1

    @event_qualifier1.setter
    def event_qualifier1(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._event_qualifier1 = value

    @property
    def event_qualifier2(self) -> str:
        return self._event_qualifier2

    @event_qualifier2.setter
    def event_qualifier2(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._event_qualifier2 = value

    @property
    def creation_date(self) -> str:
        return self._creation_date

    @creation_date.setter
    def creation_date(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._creation_date = value.upper()

    @property
    def orig_creation_date(self) -> str:
        return self._orig_creation_date

    @orig_creation_date.setter
    def orig_creation_date(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._orig_creation_date = value.upper()

    @property
    def start_date_time(self) -> str:
        return self._start_date_time

    @start_date_time.setter
    def start_date_time(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._start_date_time = value.upper()

    @property
    def end_date_time(self) -> str:
        return self._end_date_time

    @end_date_time.setter
    def end_date_time(self, value: str) -> NoReturn:
        value = value.strip("\' ")
        self._end_date_time = value.upper()

    @property
    def initial_latitude(self) -> float:
        return self._initial_latitude

    @initial_latitude.setter
    def initial_latitude(self, value: float) -> NoReturn:
        self._initial_latitude = value

    @property
    def initial_longitude(self) -> float:
        return self._initial_longitude

    @initial_longitude.setter
    def initial_longitude(self, value: float) -> NoReturn:
        self._initial_longitude = value

    @property
    def end_latitude(self) -> float:
        return self._end_latitude

    @end_latitude.setter
    def end_latitude(self, value: float) -> NoReturn:
        self._end_latitude = value

    @property
    def end_longitude(self) -> float:
        return self._end_longitude

    @end_longitude.setter
    def end_longitude(self, value: float) -> NoReturn:
        self._end_longitude = value

    @property
    def min_depth(self) -> float:
        return self._min_depth

    @min_depth.setter
    def min_depth(self, value: float) -> NoReturn:
        self._min_depth = value

    @property
    def max_depth(self) -> float:
        return self._max_depth

    @max_depth.setter
    def max_depth(self, value: float) -> NoReturn:
        self._max_depth = value

    @property
    def sampling_interval(self) -> float:
        return self._sampling_interval

    @sampling_interval.setter
    def sampling_interval(self, value: float) -> NoReturn:
        self._sampling_interval = value

    @property
    def sounding(self) -> float:
        return self._sounding

    @sounding.setter
    def sounding(self, value: float) -> NoReturn:
        self._sounding = value

    @property
    def depth_off_bottom(self) -> float:
        return self._depth_off_bottom

    @depth_off_bottom.setter
    def depth_off_bottom(self, value: float) -> NoReturn:
        self._depth_off_bottom = value

    @property
    def station_name(self) -> str:
        return self._station_name

    @station_name.setter
    def station_name(self, value: str) -> NoReturn:
        self._station_name = f'{value}'

    @property
    def set_number(self) -> str:
        return self._set_number

    @set_number.setter
    def set_number(self, value: str) -> NoReturn:
        self._set_number = f'{value}'

    @property
    def event_comments(self) -> list:
        return self._event_comments

    @event_comments.setter
    def event_comments(self, value: list) -> NoReturn:
        self._event_comments = value
    
    def set_event_comment(self, event_comment: str, 
                          comment_number: int = 0) -> None:
        event_comment = event_comment.strip("\'")
        number_of_comments = len(self.event_comments)
        if comment_number == 0 and number_of_comments >= 0:
            self._event_comments.append(f'{event_comment}')
        elif comment_number <= number_of_comments and number_of_comments > 0:
            self._event_comments[comment_number-1] = f'{event_comment}'
        else:
            raise ValueError("The 'event_comment' number is incorrect.")

    def populate_object(self, event_fields: list):
        for header_line in event_fields:
            tokens = header_line.split('=', maxsplit=1)
            event_dict = odfutils.list_to_dict(tokens)
            for key, value in event_dict.items():
                key = key.strip()
                if str(value):
                    value = value.strip()
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
                        self.initial_latitude = value
                    case 'INITIAL_LONGITUDE':
                        self.initial_longitude = value
                    case 'END_LATITUDE':
                        self.end_latitude = value
                    case 'END_LONGITUDE':
                        self.end_longitude = value
                    case 'MIN_DEPTH':
                        self.min_depth = value
                    case 'MAX_DEPTH':
                        self.max_depth = value
                    case 'SAMPLING_INTERVAL':
                        self.sampling_interval = value
                    case 'SOUNDING':
                        self.sounding = value
                    case 'DEPTH_OFF_BOTTOM':
                        self.depth_off_bottom = value
                    case 'STATION_NAME':
                        self.station_name = value
                    case 'SET_NUMBER':
                        self.set_number = value
                    case 'EVENT_COMMENTS':
                        self.event_comments = value
        return self

    def print_object(self) -> str:
        event_header_output = "EVENT_HEADER\n"
        event_header_output += f"  DATA_TYPE = '{self.data_type}'\n"
        event_header_output += f"  EVENT_NUMBER = '{self.event_number}'\n"
        event_header_output += f"  EVENT_QUALIFIER1 = '{self.event_qualifier1}'\n"
        event_header_output += f"  EVENT_QUALIFIER2 = '{self.event_qualifier2}'\n"
        event_header_output += f"  CREATION_DATE = '{odfutils.check_datetime(self.creation_date)}'\n"
        event_header_output += f"  ORIG_CREATION_DATE = '{odfutils.check_datetime(self.orig_creation_date)}'\n"
        event_header_output += f"  START_DATE_TIME = '{odfutils.check_datetime(self.start_date_time)}'\n"
        event_header_output += f"  END_DATE_TIME = '{odfutils.check_datetime(self.end_date_time)}'\n"
        if self.initial_latitude == BaseHeader.null_value:
            event_header_output += f"  INITIAL_LATITUDE = {self.initial_latitude}\n"
        else:
            event_header_output += f"  INITIAL_LATITUDE = {self.initial_latitude:.2f}\n"
        if self.initial_longitude == BaseHeader.null_value:
            event_header_output += f"  INITIAL_LONGITUDE = {self.initial_longitude}\n"
        else:
            event_header_output += f"  INITIAL_LONGITUDE = {self.initial_longitude:.2f}\n"
        if self.end_latitude == BaseHeader.null_value:
            event_header_output += f"  END_LATITUDE = {self.end_latitude}\n"
        else:
            event_header_output += f"  END_LATITUDE = {self.end_latitude:.2f}\n"
        if self.end_longitude == BaseHeader.null_value:
            event_header_output += f"  END_LONGITUDE = {self.end_longitude}\n"
        else:
            event_header_output += f"  END_LONGITUDE = {self.end_longitude:.2f}\n"
        if self.min_depth == BaseHeader.null_value:
            event_header_output += f"  MIN_DEPTH = {self.min_depth}\n"
        else:
            event_header_output += f"  MIN_DEPTH = {self.min_depth:.2f}\n"
        if self.max_depth == BaseHeader.null_value:
            event_header_output += f"  MAX_DEPTH = {self.max_depth}\n"
        else:
            event_header_output += f"  MAX_DEPTH = {self.max_depth:.2f}\n"
        event_header_output += f"  SAMPLING_INTERVAL = {self.sampling_interval}\n"
        if self.sounding == BaseHeader.null_value:
            event_header_output += f"  SOUNDING = {self.sounding}\n"
        else:
            event_header_output += f"  SOUNDING = {self.sounding:.2f}\n"
        if self.depth_off_bottom == BaseHeader.null_value:
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
        event = EventHeader()
        print(event.print_object())
        event.creation_date = '2021-03-25T00:00:00'
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
        event.log_message('station_name', event.station_name, 'STN_01')
        event.station_name = 'STN_01' 
        event.set_number = '001'
        event.set_event_comment('Good cast!')
        print(event.print_object())
        
        for log_entry in BaseHeader.shared_log_list:
            print(log_entry)


if __name__ == "__main__":

    EventHeader.main()