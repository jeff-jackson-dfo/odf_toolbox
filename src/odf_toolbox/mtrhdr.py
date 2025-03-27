from datetime import datetime
import pandas as pd
import os
from icecream import ic

from odf_toolbox.lookup_parameter import lookup_parameter
from odf_toolbox.odfhdr import OdfHeader
from odf_toolbox.parameterhdr import ParameterHeader
from odf_toolbox.historyhdr import HistoryHeader

class MtrHeader(OdfHeader):
    """
    Mtr Class: subclass of OdfHeader.

    This class is responsible for storing the metadata and data associated 
    with a moored thermograph (MTR).
    """

    def __init__(self):
        """
        Method that initializes an Mtr class object.
        """
        super().__init__()
        self._date_format = r'%Y-%m-%d'
        self._time_format = r'%H:%M:%S'
        self._sytm_format = r'%d-%b-%Y %H:%M:%S.%f'

    def get_sytm_format(self) -> str:
        return self._sytm_format
    
    def get_date_format(self) -> str:
        return self._date_format
    
    def get_time_format(self) -> str:
        return self._time_format

    def generate_creation_date(self) -> str:
        """ Generate a creation date in SYTM format. """
        creation_date = datetime.now().strftime(self._sytm_format)[:-4].upper()
        return creation_date

    def start_date_time(self, df: pd.Series) -> datetime:
        """ Retrieve the first date-time value from the data frame. """
        start_date = datetime.strptime(df['date'].iloc[0], self._date_format)
        start_time = datetime.strptime(df['time'].iloc[0], self._time_format).time()
        start_date_time = datetime.combine(start_date, start_time)
        return start_date_time

    def end_date_time(self, df: pd.Series) -> datetime:
        """ Retrieve the last date-time value from the data frame. """
        end_date = datetime.strptime(df['date'].iloc[-1], self._date_format)
        end_time = datetime.strptime(df['time'].iloc[-1], self._time_format).time()
        end_date_time = datetime.combine(end_date, end_time)
        return end_date_time

    def sampling_interval(self, df: pd.Series) -> int:
        """ Compute the time interval between the first two date-time values. """
        date1 = datetime.strptime(df['date'].iloc[0], self._date_format)
        time1 = datetime.strptime(df['time'].iloc[0], self._time_format).time()
        datetime1 = datetime.combine(date1, time1)
        date2 = datetime.strptime(df['date'].iloc[1], self._date_format)
        time2 = datetime.strptime(df['time'].iloc[1], self._time_format).time()
        datetime2 = datetime.combine(date2, time2)
        time_interval = datetime2 - datetime1
        time_interval = time_interval.seconds
        return time_interval

    def create_sytm(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Updated the data frame with the proper SYTM column. """
        df['dates'] = df['date'].apply(lambda x: datetime.strptime(x, self._date_format).date())
        df['dates'] = df['dates'].astype("string")
        df['times'] = df['time'].apply(lambda x: datetime.strptime(x, self._time_format).time())
        df['times'] = df['times'].astype("string")
        df['datetimes'] = df['dates'] + ' ' + df['times']
        df = df.drop(columns=['date', 'time', 'dates', 'times'], axis=1)
        df['datetimes'] = pd.to_datetime(df['datetimes'])
        df['sytm'] = df['datetimes'].apply(lambda x: datetime.strftime(x, self._sytm_format)).str.upper()
        df = df.drop('datetimes', axis=1)
        df['sytm'] = df['sytm'].str[:-4]
        df['sytm'] = df['sytm'].apply(lambda x: "'" + str(x) + "'")
        return df

    def populate_parameter_headers(self, df: pd.DataFrame):
        """ Populate the parameter headers and the data object. """
        parameter_list = list()
        print_formats = dict()
        number_of_rows = df.count().iloc[0]
        for column in df.columns:
            parameter_header = ParameterHeader()
            number_null = int(df[column].isnull().sum())
            number_valid = int(number_of_rows - number_null)
            if column == 'sytm':
                parameter_info = lookup_parameter('SYTM')
                parameter_header.set_type('SYTM', read_operation=True)
                parameter_header.set_name(parameter_info.get('description'), read_operation=True)
                parameter_header.set_units(parameter_info.get('units'), read_operation=True)
                parameter_header.set_code('SYTM_01', read_operation=True)
                parameter_header.set_null_value('17-NOV-1858 00:00:00.00', read_operation=True)
                parameter_header.set_print_field_width(parameter_info.get('print_field_width'), read_operation=True)
                parameter_header.set_print_decimal_places(parameter_info.get('print_decimal_places'), read_operation=True)
                parameter_header.set_angle_of_section('-99.0', read_operation=True)
                parameter_header.set_magnetic_variation('-99.0', read_operation=True)
                parameter_header.set_depth('-99.0', read_operation=True)
                min_date = df[column].iloc[0].strip("\'")
                max_date = df[column].iloc[-1].strip("\'")
                parameter_header.set_minimum_value(min_date, read_operation=True)
                parameter_header.set_maximum_value(max_date, read_operation=True)
                parameter_header.set_number_valid(number_valid, read_operation=True)
                parameter_header.set_number_null(number_null, read_operation=True)
                parameter_list.append('SYTM_01')
                print_formats['SYTM_01'] = (parameter_header.get_print_field_width())
            elif column == 'temperature':
                parameter_info = lookup_parameter('TE90')
                parameter_header.set_type('DOUB', read_operation=True)        
                parameter_header.set_name(parameter_info.get('description'), read_operation=True)
                parameter_header.set_units(parameter_info.get('units'), read_operation=True)
                parameter_header.set_code('TE90_01', read_operation=True)
                parameter_header.set_null_value('-99.0', read_operation=True)
                parameter_header.set_print_field_width(parameter_info.get('print_field_width'), read_operation=True)
                parameter_header.set_print_decimal_places(parameter_info.get('print_decimal_places'), read_operation=True)
                parameter_header.set_angle_of_section('-99.0', read_operation=True)
                parameter_header.set_magnetic_variation('-99.0', read_operation=True)
                parameter_header.set_depth('-99.0', read_operation=True)
                min_temp = df[column].min()
                max_temp = df[column].max()
                parameter_header.set_minimum_value(min_temp, read_operation=True)
                parameter_header.set_maximum_value(max_temp, read_operation=True)
                parameter_header.set_number_valid(number_valid, read_operation=True)
                parameter_header.set_number_null(number_null, read_operation=True)
                parameter_list.append('TE90_01')
                print_formats['TE90_01'] = (f"{parameter_header.get_print_field_width()}."
                                            f"{parameter_header.get_print_decimal_places()}")
            
            # Add the new parameter header to the list.
            self.parameter_headers.append(parameter_header)

        # Update the data object.
        self.data.set_parameter_list(parameter_list)
        self.data.set_print_formats(print_formats)
        self.data.set_data_frame(df)
        return self
    
    @staticmethod
    def read_mtr(mtrfile: str) -> dict:
        """
        Read an MTR data file and return a pandas DataFrame.
        """
        
        mtr_dict = dict()

        # Read the data lines from the MTR file.
        dfmtr = pd.read_table(mtrfile, sep=',', header=None, encoding='iso8859_1', skiprows=8)
        
        # rename the columns
        dfmtr.columns = ['date', 'time', 'temperature']

        mtr_dict['df'] = dfmtr

        # Get the instrument type and gauge (serial number) from the MTR file.
        with open(mtrfile, 'r', encoding='iso8859_1') as f:
            for i in range(8):
                line = f.readline()
                if 'Source Device:' in line:
                    info = line.split(':')[1]
                    inst_model = info.rsplit('-', 1)[0]
                    gauge = info.split('-')[-1].strip()
                    break
        
        mtr_dict['inst_model'] = inst_model
        mtr_dict['gauge'] = gauge
        return mtr_dict

    @staticmethod
    def read_metadata(metafile: str) -> pd.DataFrame:
        """
        Read a Metadata file and return a pandas DataFrame.
        """
        # read the file
        dfmeta = pd.read_table(metafile, encoding='iso8859_1')

        # Change some column types.
        dfmeta['LFA'].astype(int)
        dfmeta['Vessel Code'].astype(int)
        dfmeta['Gauge'].astype(int)
        dfmeta['Soak Days'].astype(int)

        # Drop some columns.
        dfmeta.drop(columns=['Date.1', 'Latitude', 'Longitude', 'Depth'], inplace=True)

        # Rename some columns.
        dfmeta.rename(columns={'Date': 'date', 'Time': 'time', 'LFA': 'lfa', 
                            'Vessel Code': 'vessel_code', 'Gauge': 'gauge', 
                            'Soak Days': 'soak_days', 
                            'Latitude (degrees)': 'latitude', 
                            'Longitude (degrees)': 'longitude',
                            'Depth (m)': 'depth', 'Temp': 'temperature'},
                            inplace=True)

        # Replace all NaN values with 12:00 in times as this is not important 
        # other than to have a time.
        dfmeta['time'] = dfmeta['time'].fillna('12:00')

        # Add a datetime column.
        dfmeta['date'] = dfmeta['date'].astype("string")
        dfmeta['time'] = dfmeta['time'].astype("string")
        datetime_str = ''
        datetimes = []
        date_format = '%B-%d-%y %H:%M'
        for i in range(len(dfmeta)):
            date_str = dfmeta['date'].iloc[i]
            time_str = dfmeta['time'].iloc[i]
            datetime_str = date_str + ' ' + time_str
            datetimes.append(datetime.strptime(datetime_str, date_format))
        dfmeta['datetime'] = datetimes
        return dfmeta

    def main():

        # Generate an empty MTR object.
        mtr = MtrHeader()

        # operator = input('Enter the name of the operator: ')
        operator = 'Jeff Jackson'

        # Change to the drive's root folder
        os.chdir('\\')
        drive = os.getcwd()
        pathlist = ['DEV', 'MTR', 'FSRS_data_2013_2014', 'LFA_27_14']
        top_folder = os.path.join(drive, *pathlist)
        os.chdir(top_folder)

        mtr_file = 'Bin4255RonFraser14.csv'
        # mtr_file = 'Minilog-T_4239_2014JayMacDonald_1.csv'
        mtr_path = os.path.join(top_folder, mtr_file)
        print(f'\nProcessing MTR file: {mtr_path}\n')

        mydict = mtr.read_mtr(mtr_path)
        df = mydict['df']
        inst_model = mydict['inst_model']
        gauge = mydict['gauge']
        print(df.head())

        metadata_file = 'LatLong LFA 27_14.txt'
        metadata_path = os.path.join(top_folder, metadata_file)
        print(f'\nProcessing metadata file: {metadata_path}\n')
        
        meta = mtr.read_metadata(metadata_path)

        print(meta.head())
        print('\n')

        mtr.cruise_header.set_country_institute_code(1899, read_operation=True)
        cruise_year = df['date'].to_string(index=False).split('-')[0]
        cruise_number = f'BCD{cruise_year}603'
        mtr.cruise_header.set_cruise_number(cruise_number, read_operation=True)
        start_date = mtr.start_date_time(df).strftime(r'%d-%b-%Y') + ' 00:00:00'
        mtr.cruise_header.set_start_date(start_date, read_operation=True)
        end_date = mtr.end_date_time(df).strftime(r'%d-%b-%Y') + ' 00:00:00'
        mtr.cruise_header.set_end_date(end_date, read_operation=True)
        mtr.cruise_header.set_organization('FSRS', read_operation=True)
        mtr.cruise_header.set_chief_scientist('Shannon Scott-Tibbetts', read_operation=True)
        mtr.cruise_header.set_cruise_description('Fishermen and Scientists Research Society', read_operation=True)
        
        mtr.event_header.set_data_type('MTR', read_operation=True)
        mtr.event_header.set_event_qualifier1(gauge, read_operation=True)
        mtr.event_header.set_event_qualifier2(str(mtr.sampling_interval(df)), read_operation=True)
        mtr.event_header.set_creation_date(mtr.generate_creation_date(), read_operation=True)
        mtr.event_header.set_orig_creation_date(mtr.generate_creation_date(), read_operation=True)
        mtr.event_header.set_start_date_time(mtr.start_date_time(df).strftime(mtr.get_sytm_format())[:-4].upper(), read_operation=True)
        mtr.event_header.set_end_date_time(mtr.end_date_time(df).strftime(mtr.get_sytm_format())[:-4].upper(), read_operation=True)
        mtr.event_header.set_initial_latitude(meta['latitude'].iloc[0], read_operation=True)
        mtr.event_header.set_initial_longitude(meta['longitude'].iloc[0], read_operation=True)
        mtr.event_header.set_end_latitude(meta['latitude'].iloc[0], read_operation=True)
        mtr.event_header.set_end_longitude(meta['longitude'].iloc[0], read_operation=True)
        mtr.event_header.set_min_depth(meta['depth'].iloc[0], read_operation=True)
        mtr.event_header.set_max_depth(meta['depth'].iloc[0], read_operation=True)
        mtr.event_header.set_event_number(str(meta['vessel_code'].iloc[0]), read_operation=True)
        mtr.event_header.set_sampling_interval(float(mtr.sampling_interval(df)), read_operation=True)
        
        if 'minilog' in inst_model.lower():
            mtr.instrument_header.set_instrument_type('MINILOG', read_operation=True)
        mtr.instrument_header.set_model(inst_model, read_operation=True)
        mtr.instrument_header.set_serial_number(gauge, read_operation=True)
        mtr.instrument_header.set_description('Temperature data logger', read_operation=True)

        history_header = HistoryHeader()
        history_header.set_creation_date(mtr.generate_creation_date(), read_operation=True)
        history_header.set_process(f'Initial file creation by {operator}', read_operation=True)
        mtr.history_headers.append(history_header)

        new_df = mtr.create_sytm(df)

        mtr = mtr.populate_parameter_headers(new_df)

        for x, column in enumerate(new_df.columns):
            code = mtr.parameter_headers[x].get_code()
            new_df.rename(columns={column: code}, inplace=True)

        mtr.update_odf()

        file_spec = mtr.generate_file_spec()
        odf_file_path = os.path.join(top_folder, file_spec + '.ODF')
        mtr.write_odf(odf_file_path, version=2)
        

if __name__ == "__main__":
    MtrHeader.main()
