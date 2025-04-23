import datetime
import pandas as pd
from icecream import ic
import re

from odf_toolbox.basehdr import BaseHeader
from odf_toolbox.compasshdr import CompassCalHeader
from odf_toolbox.cruisehdr import CruiseHeader
from odf_toolbox.eventhdr import EventHeader
from odf_toolbox.generalhdr import GeneralCalHeader
from odf_toolbox.historyhdr import HistoryHeader
from odf_toolbox.instrumenthdr import InstrumentHeader
from odf_toolbox.meteohdr import MeteoHeader
from odf_toolbox.parameterhdr import ParameterHeader
from odf_toolbox.polynomialhdr import PolynomialCalHeader
from odf_toolbox.qualityhdr import QualityHeader
from odf_toolbox.recordhdr import RecordHeader
from odf_toolbox.records import DataRecords
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel

class OdfHeader(BaseModel, BaseHeader):
    """
    Odf Header Class

    This class is responsible for storing the metadata associated with an ODF object (file).

    It contains a series of header subclasses that store metadata associated with various aspects of the ODF object.

    """

    def __init__(self,
                 file_specification: str = '',
                 odf_specification_version: int = 2,
                 cruise_header: CruiseHeader = None,
                 event_header: EventHeader = None,
                 meteo_header: MeteoHeader = None,
                 instrument_header: InstrumentHeader = None,
                 quality_header: QualityHeader = None,
                 general_cal_headers: list = None,
                 compass_cal_headers: list = None,
                 polynomial_cal_headers: list = None,
                 history_headers: list = None,
                 parameter_headers: list = None,
                 record_header: RecordHeader = None,
                 data: DataRecords = None):
        """
        Method that initializes an OdfHeader class object.
        """
        super().__init__()
        self.file_specification = file_specification
        self.odf_specification_version = odf_specification_version
        self.cruise_header = cruise_header if cruise_header is not None else CruiseHeader()
        self.event_header = event_header if event_header is not None else EventHeader()
        self.meteo_header = meteo_header if meteo_header is not None else MeteoHeader()
        self.instrument_header = instrument_header if instrument_header is not None else InstrumentHeader()
        self.quality_header = quality_header if quality_header is not None else QualityHeader()
        self.general_cal_headers = general_cal_headers if general_cal_headers is not None else []
        self.compass_cal_headers = compass_cal_headers if compass_cal_headers is not None else []
        self.polynomial_cal_headers = polynomial_cal_headers if polynomial_cal_headers is not None else []
        self.history_headers = history_headers if history_headers is not None else []
        self.parameter_headers = parameter_headers if parameter_headers is not None else []
        self.record_header = record_header if record_header is not None else RecordHeader()
        self.data = data if data is not None else DataRecords()

    def log_message(self, message: str, type: str = 'self'):
        if type == "self":
            super().log_message(f"In ODF Header field {message}")
        elif type == "base":
            super().log_message(message)

    @property
    def file_specification(self) -> str:
        """
        Returns the file specification from the ODF_HEADER of an OdfHeader class object.

        Returns
        -------
        file_specification (str) :
            The file name and possibly path of an OdfHeader object (default is an empty string).
        """
        return self._file_specification

    @file_specification.setter
    def file_specification(self, value: str) -> NoReturn:
        """
        Sets the file specification in the ODF_HEADER of an OdfHeader class object.

        Parameters
        ----------
        value : str
            The file name and possibly path of the OdfHeader object (default is an empty string).
        """
        value = value.strip("\' ")
        self._file_specification = value

    @property
    def odf_specification_version(self) -> float:
        """
        Returns the file specification from the ODF_HEADER of an OdfHeader class object.

        Returns
        -------
        odf_specification_version (float) :
            The file name and possibly path of an OdfHeader object (default is an empty string).
        """
        return self._odf_specification_version

    @odf_specification_version.setter
    def odf_specification_version(self, value: float) -> NoReturn:
        """
        Sets the file specification for the ODF_HEADER of an OdfHeader class object.

        Parameters
        ----------
        value : float
            The version of the ODF specification used to generate this file.
        """
        self._odf_specification_version = value

    @property
    def cruise_header(self) -> CruiseHeader:
        return self._cruise_header

    @cruise_header.setter
    def cruise_header(self, value: CruiseHeader) -> NoReturn:
        self._cruise_header = value

    @property
    def event_header(self) -> EventHeader:
        return self._event_header

    @event_header.setter
    def event_header(self, value: EventHeader) -> NoReturn:
        self._event_header = value

    @property
    def meteo_header(self) -> MeteoHeader:
        return self._meteo_header

    @meteo_header.setter
    def meteo_header(self, value: MeteoHeader) -> NoReturn:
        self._meteo_header = value

    @property
    def instrument_header(self) -> InstrumentHeader:
        return self._instrument_header

    @instrument_header.setter
    def instrument_header(self, value: InstrumentHeader) -> NoReturn:
        self._instrument_header = value

    @property
    def quality_header(self) -> QualityHeader:
        return self._quality_header

    @quality_header.setter
    def quality_header(self, value: QualityHeader) -> NoReturn:
        self._quality_header = value

    @property
    def general_cal_headers(self) -> list:
        return self._general_cal_headers

    @general_cal_headers.setter
    def general_cal_headers(self, value: list) -> NoReturn:
        self._general_cal_headers = value

    @property
    def compass_cal_headers(self) -> list:
        return self._compass_cal_headers

    @compass_cal_headers.setter
    def compass_cal_headers(self, value: list) -> NoReturn:
        self._compass_cal_headers = value

    @property
    def polynomial_cal_headers(self) -> list:
        return self._polynomial_cal_headers

    @polynomial_cal_headers.setter
    def polynomial_cal_headers(self, value: list) -> NoReturn:
        self._polynomial_cal_headers = value

    @property
    def history_headers(self) -> list:
        return self._history_headers

    @history_headers.setter
    def history_headers(self, value: list) -> NoReturn:
        self._history_headers = value

    @property
    def parameter_headers(self) -> list:
        return self._parameter_headers

    @parameter_headers.setter
    def parameter_headers(self, value: list) -> NoReturn:
        self._parameter_headers = value

    @property
    def record_header(self) -> RecordHeader:
        return self._record_header

    @record_header.setter
    def record_header(self, value: RecordHeader) -> NoReturn:
        self._record_header = value

    @property
    def data(self) -> DataRecords:
        return self._data

    @data.setter
    def data(self, value: DataRecords) -> NoReturn:
        self._data = value

    def populate_object(self, odf_dict: dict):
        """
        Populates the ODF_HEADER of an OdfHeader class object.

        Parameters
        ----------
        odf_dict : dict
            key, value pairs containing the info for the ODF_HEADER.

        """
        for key, value in odf_dict.items():
            match key.strip():
                case 'FILE_SPECIFICATION':
                    self._file_specification = value.strip()
                case 'ODF_SPECIFICATION_VERSION':
                    self._odf_specification_version = value.strip()
        return self

    def print_object(self, file_version: float = 2) -> str:
        """
        Prints the ODF_HEADER of the OdfHeader object

        Args:
            file_version : float, optional
        """

        # Add the modifications done to the odfHeader instance before outputting it.
        self.add_log_to_history()

        odf_output = ""
        if file_version == 2:
            self.set_odf_specification_version(2.0)
            odf_output = "ODF_HEADER,\n"
            odf_output += f"  FILE_SPECIFICATION = '{odfutils.check_string(self.get_file_specification())}',\n"
            odf_output += odfutils.add_commas(self.cruise_header.print_object())
            odf_output += odfutils.add_commas(self.event_header.print_object())
            if self.meteo_header is not None:
                odf_output += odfutils.add_commas(self.meteo_header.print_object())
            odf_output += odfutils.add_commas(self.instrument_header.print_object())
            if self.quality_header is not None:
                odf_output += odfutils.add_commas(self.quality_header.print_object())
            for general in self.general_cal_headers:
                odf_output += odfutils.add_commas(general.print_object())
            for poly in self.polynomial_cal_headers:
                odf_output += odfutils.add_commas(poly.print_object())
            for compass in self.compass_cal_headers:
                odf_output += odfutils.add_commas(compass.print_object())
            for hist in self.history_headers:
                odf_output += odfutils.add_commas(hist.print_object())
            for param in self.parameter_headers:
                odf_output += odfutils.add_commas(param.print_object())
            odf_output += odfutils.add_commas(self.record_header.print_object())
            odf_output += "-- DATA --\n"
            odf_output += self.data.print_object_old_style()
        elif file_version >= 3:
            self.set_odf_specification_version(3.0)
            odf_output = "ODF_HEADER\n"
            odf_output += f"  FILE_SPECIFICATION = '{odfutils.check_string(self.get_file_specification())}'\n"
            odf_output += (f"  ODF_SPECIFICATION_VERSION = "
                           f"{odfutils.check_float(self.get_odf_specification_version())}\n")
            odf_output += self.cruise_header.print_object()
            odf_output += self.event_header.print_object()
            if self.meteo_header is not None:
                odf_output += self.meteo_header.print_object()
            if self.quality_header is not None:
                odf_output += self.quality_header.print_object()
            for general in self.general_cal_headers:
                odf_output += general.print_object()
            for poly in self.polynomial_cal_headers:
                odf_output += poly.print_object()
            odf_output += self.instrument_header.print_object()
            for compass in self.compass_cal_headers:
                odf_output += compass.print_object()
            for hist in self.history_headers:
                odf_output += hist.print_object()
            for param in self.parameter_headers:
                odf_output += param.print_object()
            odf_output += self.record_header.print_object()
            odf_output += "-- DATA --\n"
            odf_output += self.data.print_object()
        return odf_output

    # def read_header(odf: Type[newOdfHeader], lines: list) -> newOdfHeader:
    def read_odf(self, odf_file_path: str):
        """
        Reads an ODF file and puts it into an OdfHeader class object.

        Parameters
        ----------
        odf_file_path : str
            The full path and filename to the ODF file to be read.

        Returns
        -------
        odf_object : OdfHeader object
            the modified OdfHeader object now containing the information from the ODF file that was read.

        Args:
            odf_file_path:
            file_path:
        """

        file_lines = odfutils.read_file_lines(odf_file_path)

        text_to_find = "_HEADER"
        header_lines_with_indices = odfutils.find_lines_with_text(file_lines, text_to_find)
        header_starts_list = list()
        header_indices = list()
        header_names = list()
        for index, line in header_lines_with_indices:
            header_indices.append(index)
            header_names.append(line.strip(" ,"))
            header_starts_list.append([index, line.strip(" ,")])
        header_blocks_df = pd.DataFrame(header_starts_list, columns=["index", "name"])

        data_line = '-- DATA --'
        data_lines_with_indices = odfutils.find_lines_with_text(file_lines, data_line)
        data_line_start = None
        for index, line in data_lines_with_indices:
            data_line_start = index + 1

        # Separate the header and data lines
        header_lines = file_lines[:data_line_start - 1]
        data_lines = file_lines[data_line_start:]

        # Get the line range for the list of fields in each header block
        header_lines = odfutils.remove_trailing_commas_and_whitespace(header_lines)
        ndf = len(header_blocks_df)
        header_field_range = pd.DataFrame(columns=["Name", "Start", "End"])
        for i in range(ndf):
            header_field_range.at[i, 'Name'] = header_blocks_df.at[i, 'name']
            header_field_range.at[i, 'Start'] = header_blocks_df.at[i, 'index'] + 1
        for i in range(ndf):
            if 0 < i < ndf - 1:
                header_field_range.at[i - 1, 'End'] = header_blocks_df.at[i, 'index'] - 1
            elif i == ndf - 1:
                header_field_range.at[i - 1, 'End'] = header_blocks_df.at[i, 'index'] - 1
                header_field_range.at[i, 'End'] = data_line_start - 1

        # Loop through the header lines, populating the OdfHeader object as it goes.
        for i in range(ndf):
            header_block = str(header_blocks_df.at[i, 'name'])
            x = header_field_range.at[i, 'Start']
            y = header_field_range.at[i, 'End']
            block_lines = header_lines[x:y + 1]
            match header_block:
                case "COMPASS_CAL_HEADER":
                    compass_cal_header = CompassCalHeader()
                    compass_cal_header.populate_object(block_lines)
                    self.compass_cal_headers.append(compass_cal_header)
                case "CRUISE_HEADER":
                    self.cruise_header = self.cruise_header.populate_object(block_lines)
                case "EVENT_HEADER":
                    self.event_header = self.event_header.populate_object(block_lines)
                case "GENERAL_CAL_HEADER":
                    general_cal_header = GeneralCalHeader()
                    general_cal_header.populate_object(block_lines)
                    self.general_cal_headers.append(general_cal_header)
                case "HISTORY_HEADER":
                    history_header = HistoryHeader()
                    history_header.populate_object(block_lines)
                    self.history_headers.append(history_header)
                case "INSTRUMENT_HEADER":
                    self.instrument_header = self.instrument_header.populate_object(block_lines)
                case "METEO_HEADER":
                    self.meteo_header = MeteoHeader()
                    self.meteo_header.populate_object(block_lines)
                case "ODF_HEADER":
                    for header_line in block_lines:
                        tokens = header_line.split('=', maxsplit=1)
                        header_fields = odfutils.split_lines_into_dict(tokens)
                        self.populate_object(header_fields)
                case "PARAMETER_HEADER":
                    parameter_header = ParameterHeader()
                    parameter_header.populate_object(block_lines)
                    self.parameter_headers.append(parameter_header)
                case "POLYNOMIAL_CAL_HEADER":
                    polynomial_cal_header = PolynomialCalHeader()
                    polynomial_cal_header.populate_object(block_lines)
                    self.polynomial_cal_headers.append(polynomial_cal_header)
                case "QUALITY_HEADER":
                    self.quality_header = QualityHeader()
                    self.quality_header.populate_object(block_lines)
                case "RECORD_HEADER":
                    self.record_header = RecordHeader()
                    self.record_header.populate_object(block_lines)
        parameter_list = list()
        parameter_formats = dict()
        for parameter in self.parameter_headers:
            parameter_code = parameter.get_code().strip("'")
            parameter_list.append(parameter_code)
            if parameter_code[0:4] == 'SYTM':
                parameter_formats[parameter_code] = f"{parameter.get_print_field_width()}"
            else:
                parameter_formats[parameter_code] = (f"{parameter.get_print_field_width()}."
                                                     f"{parameter.get_print_decimal_places()}")
        self.data.populate_object(parameter_list, parameter_formats, data_lines)
        return self

    def update_odf(self) -> None:
        if self.record_header.get_num_calibration() != len(self.polynomial_cal_headers):
            self.record_header.set_num_calibration(len(self.polynomial_cal_headers))
        if self.record_header.get_num_history() != len(self.history_headers):
            self.record_header.set_num_history(len(self.history_headers))
        if self.record_header.get_num_swing() != len(self.compass_cal_headers):
            self.record_header.set_num_swing(len(self.compass_cal_headers))
        if self.record_header.get_num_param() != len(self.parameter_headers):
            self.record_header.set_num_param(len(self.parameter_headers))
        if self.record_header.get_num_cycle() != len(self.data):
            self.record_header.set_num_cycle(len(self.data))
        self.set_file_specification(self.generate_file_spec())

    def write_odf(self, odf_file_path: str, version: float = 2) -> None:
        """ Write the ODF file to disk. """
        odf_file_text = self.print_object(file_version=version)
        file1 = open(odf_file_path, "w")
        file1.write(odf_file_text)
        file1.close()
        print(f"ODF file written to {odf_file_path}\n")

    def add_history(self):
        nhh = HistoryHeader()
        dt = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S.%f").upper()
        nhh.set_creation_date(dt[:-4])
        self.history_headers.append(nhh)

    def add_to_history(self, history_comment):
        if history_comment is not None:
            if len(self.history_headers) > 0:
                self.history_headers[-1].add_process(history_comment)
            else:
                self.history_headers.append(history_comment)

    def add_log_to_history(self):
        # Access the log records stored in the custom handler
        for log_entry in self.shared_log_list:
            self.add_to_history(log_entry)

    def add_to_log(self, message):
        # Access the log records stored in the custom handler
        self.shared_log_list.append(message)

    def update_parameter(self, parameter_code: str, attribute: str, value):
        assert isinstance(parameter_code, str), \
               f"Input value is not of type str: {parameter_code}"
        assert isinstance(attribute, str), \
               f"Input value is not of type str: {attribute}"
        codes = self.data.get_parameter_list()
        assert isinstance(codes, list), \
               f"Input value is not of type list: {codes}"
        if isinstance(value, str):
            eval(f"self.parameter_headers[codes.index(parameter_code)].set_{attribute}('{value}')")
        else:
            eval(f"self.parameter_headers[codes.index(parameter_code)].set_{attribute}({value})")

    def get_parameter_codes(self) -> list:
        parameter_codes = list()
        for ph1 in self.parameter_headers:
            parameter_codes.append(ph1.get_code())
        return parameter_codes

    def get_parameter_names(self) -> list:
        parameter_names = list()
        for ph2 in self.parameter_headers:
            # ic(ph2.get_name())
            parameter_names.append(ph2.get_name())
        return parameter_names

    def generate_file_spec(self):
        dt = self.event_header.get_data_type().strip("'")
        cn = self.cruise_header.get_cruise_number().strip("'")
        en = self.event_header.get_event_number().strip("'")
        eq1 = self.event_header.get_event_qualifier1().strip("'")
        eq2 = self.event_header.get_event_qualifier2().strip("'")
        file_spec = f"{dt}_{cn}_{en}_{eq1}_{eq2}"
        file_spec = file_spec
        return file_spec

    def fix_parameter_codes(self, new_codes: list = []):

        # Get the list of parameter names and the data frame in case names need to be fixed.
        df = self.data.get_data_frame()
        if new_codes == []:

            # Check if the parameter codes are in the correct format. If they are not then fix them.
            codes = self.data.get_parameter_list()

            # Loop through the list of parameter codes and fix any that require it.
            for p, pcode in enumerate(codes):
                ic(pcode)
                expected_format = '[A-Z]{4}[_]{1}[0-9]{2}'
                expected_match = re.compile(expected_format)
                if expected_match.findall(pcode) == []:
                    new_pcode = input(f"Please enter the correct code name (e.g. TEMP_01) for {pcode} : ")
                    new_codes.append(new_pcode)
                    df.rename(columns={pcode: new_pcode})
                    self.parameter_headers[p].set_code(new_pcode)

            # Fix the Polynomial_Cal_Headers if required.
            if self.polynomial_cal_headers:
                self.fix_polynomial_codes(codes, new_codes)

            # Assign the revised data frame back to the odf object.
            self.data.set_data_frame(df)
        
        else:

            old_codes = df.columns.to_list()
            df.columns = new_codes
            self.data.set_data_frame(df)
            self.data.set_parameter_list(new_codes)
            nparams = len(self.get_parameter_codes())
            for j in range(nparams):
                self.parameter_headers[j].set_code(new_codes[j])

            # Fix the Polynomial_Cal_Headers if required.
            if self.polynomial_cal_headers:
                self.fix_polynomial_codes(old_codes, new_codes)
        
        return self
    
    def fix_polynomial_codes(self, old_codes: list, new_codes: list):
        for i, pch in enumerate(self.polynomial_cal_headers):

            # Find the Polynomial_Cal_Header Code in old_codes and replace it with the corresponding code from new_codes.
            poly_code = pch.get_parameter_code()
            try:
                # This poly_code may have actually been a parameter_name instead of a parameter_code.
                # Check the parameter names and if there is a match then assign the parameter code as the polynomial code.
                pnames = self.get_parameter_names()
                pnames = [x.replace('"', '') for x in pnames]
                if poly_code in pnames:
                    self.polynomial_cal_headers[i].set_parameter_code(new_codes[i])
            except Exception as e:
                print(f"Item {poly_code} not found in old_codes list.")
        return self

    def is_parameter_code(self, code: str) -> bool:
        """
        IS_PARAMETER_CODE: Check if a parameter code is in the ODF object.

        Creation Date: 24-SEP-2014
        Last Updated: 17-MAR-2025
        """
        codes = self.get_parameter_codes()
        return code in codes

    @staticmethod
    def null2empty(df: pd.DataFrame) -> pd.DataFrame:
        """
        null2empty: replaces numeric null values (-99) with None values in the input Pandas data frame.
        """
        new_df = df.replace(-99, None, inplace=False)
        return new_df
                

def main():

    odf = OdfHeader()

    my_path = 'C:\\DEV\\GitHub\\odf_toolbox\\tests\\'
    # my_file = 'CTD_2000037_102_1_DN.ODF'
    my_file = 'CTD_91001_1_1_DN.ODF'
    # my_file = 'CTD_SCD2022277_002_01_DN.ODF'
    # my_file = 'file_with_leading_spaces.ODF'
    # my_file = 'file_with_null_data_values.ODF'
    odf.read_odf(my_path + my_file)

    # Add a new History Header to record the modifications that are made.
    odf.add_history()
    user = 'Jeff Jackson'
    odf.add_to_log(f'{user} made the following modifications to this file:')

    # Modify some of the odf metadata
    # odf.cruise_header.set_organization('DFO BIO')
    # odf.cruise_header.set_chief_scientist('GLEN HARRISON')
    odf.cruise_header.set_start_date('01-APR-2022 00:00:00')
    odf.cruise_header.set_end_date('31-OCT-2022 00:00:00')
    # odf.cruise_header.set_platform('HUDSON')
    # odf.event_header.set_station_name('AR7W_15')

    # Prior to loading data into an Oracle database, the null values need to be replaced with None values.
    new_df = odf.null2empty(odf.data.get_data_frame())
    odf.data.set_data_frame(new_df)

    # Remove the CRAT_01 parameter.
    # from odf_toolbox.remove_parameter import remove_parameter
    # odf = remove_parameter(odf, 'CRAT_01')

    # for meteo_comment in odf.meteo_header.get_meteo_comments():
    #     ic(meteo_comment)

    # Retrieve the data from the input ODF structure.
    data = odf.data.get_data_frame()

    # Get the number of data rows and columns.
    nrows, ncols = data.shape

    # Retrieve the Parameter Headers from the input ODF structure.
    parameter_headers = odf.parameter_headers
    parameter_codes = odf.get_parameter_codes()

    sytm_index = [i for i,pcode in enumerate(parameter_codes) if pcode[0:4] == 'SYTM']
    if sytm_index != []:
        sytm_index = sytm_index[0]

    for j, parameter_header in enumerate(parameter_headers):

        parameter_code = parameter_header.get_code()
        parameter_code_short, sensor_number = parameter_code.split("_")
        sensor_number = float(sensor_number)          

        if data.loc[:, parameter_code].isnull().all():

            # Suggest removing parameter columns that only contain 
            # null values.
            print(f'Should the data for {parameter_code} be deleted from '
                    'the ODF structure since it only contains NULL values?')

        # Loop through the data records. 
        for r in range(0, nrows):
            # ic(type(data.loc[r].iloc[j]))
            value = data.loc[r].iloc[j]
            # print(f'row {r}, column {j} has value {value} with type {type(value)}')

        # if f"Q{parameter_code}" in parameter_codes:
        #     qfcode = f"Q{parameter_code}"
        #     ic(qfcode)
        #     print(data[qfcode])

    # new_param_list = ['PRES_01', 'TEMP_01', 'CRAT_01', 'PSAL_01', 'NETR_01', 'FLOR_01', 'OTMP_01', 'OPPR_01', 'DOXY_01']
    # odf.fix_parameter_codes(new_param_list)
    # odf.fix_parameter_codes()

    # old_codes = odf.get_parameter_codes()

    # from datetime import datetime
    # now: datetime = datetime.now()
    # current_date_time = f'{now:%d-%b-%Y %H:%M:%S.%f}'.upper()
    # odf.event_header.set_original_creation_date(current_date_time)
    # print(odf.event_header.get_original_creation_date())

    # codes = odf.get_parameter_codes()
    # if 'SYTM_01' in codes:
    #     odf.update_parameter('SYTM_01', 'units', 'GMT')

    # odf.cruise_header.set_chief_scientist('W GLEN HARRISON')
    # odf.event_header.set_event_comments("The wind was very strong during this operation.")

    odf.update_odf()

    # Write the ODF file to disk.
    odf_file_text = odf.print_object(file_version=3)
    spec = odf.generate_file_spec()
    out_file = f"{spec}.ODF"
    odf.write_odf(my_path + out_file, version=3)


if __name__ == '__main__':    
    
    main()