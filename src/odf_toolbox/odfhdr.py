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

import pandas as pd
import datetime


class OdfHeader:
    """
    Odf Header Class

    This class is responsible for storing the metadata associated with an ODF object (file).

    It contains a series of header subclasses that store metadata associated with various aspects of the ODF object.

    """

    def __init__(self):
        """
        Method that initializes an OdfHeader class object.
        """
        self._file_specification = "''"
        self._odf_specification_version = 3
        self.cruise_header = CruiseHeader()
        self.event_header = EventHeader()
        self.meteo_header = None
        self.instrument_header = InstrumentHeader()
        self.quality_header = None
        self.general_cal_headers = []
        self.compass_cal_headers = []
        self.polynomial_cal_headers = []
        self.history_headers = []
        self.parameter_headers = []
        self.record_header = RecordHeader()
        self.data = DataRecords()

    def get_file_specification(self) -> str:
        """
        Returns the file specification from the ODF_HEADER of an OdfHeader class object.

        Returns
        -------
        file_specification (str) :
            The file name and possibly path of an OdfHeader object (default is an empty string).
        """
        return self._file_specification

    def set_file_specification(self, value: str, read_operation: bool = False) -> None:
        """
        Sets the file specification in the ODF_HEADER of an OdfHeader class object.

        Parameters
        ----------
        value : str
            The file name and possibly path of the OdfHeader object (default is an empty string).
        read_operation: bool (False)
        """
        assert isinstance(value, str), \
               f"Input value is not of type str: {value}"
        if not read_operation:
            odfutils.logger.info(f'Odf_Header.File_Specification changed from {self._file_specification} to {value}')
        self._file_specification = value

    def get_odf_specification_version(self) -> float:
        """
        Returns the file specification from the ODF_HEADER of an OdfHeader class object.

        Returns
        -------
        odf_specification_version (float) :
            The file name and possibly path of an OdfHeader object (default is an empty string).
        """
        return self._odf_specification_version

    def set_odf_specification_version(self, value: float, read_operation: bool = False):
        """
        Sets the file specification for the ODF_HEADER of an OdfHeader class object.

        Parameters
        ----------
        value : float
            The version of the ODF specification used to generate this file.
        read_operation: bool (False)

        """
        # convert input argument to float
        try:
            value = float(value)
            assert isinstance(value, float), \
                f"Input value is not of type float: {value}"
        except ValueError:
            f"Input value could not be successfully converted to type float: {value}"
        if not read_operation:
            odfutils.logger.info(
                f'Odf_Header.Odf_Specification_version changed from {self._odf_specification_version} to {value}')

        self._odf_specification_version = value

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
                    self.set_file_specification(value.strip(), read_operation=True)
                case 'ODF_SPECIFICATION_VERSION':
                    self.set_odf_specification_version(value.strip(), read_operation=True)
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
                           f"{odfutils.check_float_value(self.get_odf_specification_version())}\n")
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

    def update_odf(self):
        self.record_header.set_num_calibration(len(self.polynomial_cal_headers))
        self.record_header.set_num_history(len(self.history_headers))
        self.record_header.set_num_swing(len(self.compass_cal_headers))
        self.record_header.set_num_param(len(self.parameter_headers))
        self.record_header.set_num_cycle(len(self.data))

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
        log_records = odfutils.list_handler.log_records
        for record in log_records:
            self.add_to_history(record)

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

    def get_parameters(self):
        params = list()
        for ph in self.parameter_headers:
            params.append(ph.get_code())
        return params

    def generate_file_spec(self):
        dt = self.event_header.get_data_type().strip("'")
        cn = self.cruise_header.get_cruise_number().strip("'")
        en = self.event_header.get_event_number().strip("'")
        eq1 = self.event_header.get_event_qualifier1().strip("'")
        eq2 = self.event_header.get_event_qualifier2().strip("'")
        file_spec = f"{dt}_{cn}_{en}_{eq1}_{eq2}"
        file_spec = file_spec
        return file_spec


if __name__ == "__main__":

    odf = OdfHeader()

    my_file_path = 'D:\\DEV\odf_toolbox\\tests\\MCM_HUD2010014_1771_1039_3600.ODF'
    # my_file_path = 'D:\\DEV\odf_toolbox\\tests\\CTD_2000037_102_1_DN.ODF'
    # my_file_path = '../../tests/IML-Example.ODF'
    # my_file_path = '../../tests/MADCP_HUD2016027_1999_3469-31_3600.ODF'
    # my_file_path = '../../tests/MCTD_GRP2019001_2104_11689_1800.ODF'

    odf.read_odf(my_file_path)

    # Modify some of the odf metadata
    odf.add_history()
    odf.cruise_header.set_organization('DFO BIO')
    odf.cruise_header.set_chief_scientist('GLEN HARRISON')
    odf.cruise_header.set_start_date('05-OCT-2010 00:00:00')
    odf.cruise_header.set_end_date('22-OCT-2010 00:00:00')
    odf.cruise_header.set_platform('HUDSON')
    odf.event_header.set_station_name('AR7W_15')

    codes = odf.get_parameters()
    if 'SYTM_01' in codes:
        odf.update_parameter('SYTM_01', 'units', 'GMT')

    cspec = odf.get_file_specification()
    cspec = cspec.strip("\'")
    spec = odf.generate_file_spec()
    if cspec != spec:
        print('cspec and spec do not match')
        odf.set_file_specification(spec)

    odf_file_text = odf.print_object(file_version=3)

    out_file = f"{spec}.ODF"
    file1 = open(out_file, "w")
    file1.write(odf_file_text)
    file1.close()
