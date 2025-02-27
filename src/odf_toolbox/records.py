import io
import pandas as pd
from odf_toolbox import odfutils
from icecream import ic

class DataRecords:
    """
    A class to represent the data records stored within an ODF object.

    Attributes:
    -----------
    DataFrame : pandas DataFrame
        a data frame containing the data for the ODF object
    ParameterList : list of strings
        list of the parameter codes associated with the ODF object
    PrintFormats : list of strings
        dictionary of the parameter code print formats

    Methods:
    -------
    __init__ :
        initialize a QualityHeader class object
    get_data_frame : pd.DataFrame
    set_data_frame : None
    get_data_record_count : int
    get_parameter_list : list
    set_parameter_list : None
    get_print_formats : dict
    set_print_formats : None
    populate_object : None
    print_object : None
    print_object_old_style : None

    """

    def __init__(self):
        self._data_frame = pd.DataFrame()
        self._parameter_list = []
        self._print_formats = {}

    def get_data_frame(self) -> pd.DataFrame:
        return self._data_frame

    def set_data_frame(self, data_frame: pd.DataFrame) -> None:
        assert isinstance(data_frame, pd.DataFrame), \
               f"Input value is not of type pd.DataFrame: {data_frame}"
        self._data_frame = data_frame

    def get_parameter_list(self) -> list:
        return self._parameter_list

    def set_parameter_list(self, parameters: list):
        assert isinstance(parameters, list), \
               f"Input value is not of type list: {parameters}"
        self._parameter_list = parameters

    def get_print_formats(self) -> dict:
        return self._print_formats

    def set_print_formats(self, formats: dict):
        assert isinstance(formats, dict), \
               f"Input value is not of type dict: {formats}"
        self._print_formats = formats

    def __len__(self):
        return len(self._data_frame)

    def populate_object(self, parameter_list: list, data_formats: dict, data_lines_list: list):
        assert isinstance(parameter_list, list), \
               f"Input value is not of type list: {parameter_list}"
        assert isinstance(data_formats, dict), \
               f"Input value is not of type dict: {data_formats}"
        assert isinstance(data_lines_list, list), \
               f"Input value is not of type list: {data_lines_list}"
        data_record_list = [odfutils.split_string_with_quotes(s) for s in data_lines_list]
        df = pd.DataFrame(columns=parameter_list, data=data_record_list)
        df = odfutils.convert_dataframe(df)
        if 'SYTM_01' in df.columns:
            df['SYTM_01'] = df['SYTM_01'].apply(lambda x: f"'{x}'")
        self.set_data_frame(df)
        self.set_parameter_list(parameter_list)
        self.set_print_formats(data_formats)
        return self

    def print_object(self) -> str:
        df = self.get_data_frame()
        plist = self.get_parameter_list()
        q_params = [s for s in plist if s.startswith("Q")]
        value = 'int'
        convert_dict = {key: value for key in q_params}
        df = df.astype(convert_dict)
        self.set_data_frame(df)
        buffer = io.StringIO()
        self.get_data_frame().to_csv(buffer, index=False, sep=",", lineterminator="\n")
        output_data_records_v3 = buffer.getvalue()
        return output_data_records_v3

    def print_object_old_style(self) -> str:
        nf = len(self.get_print_formats().items())
        key_number = 0
        formatter = (f"self.get_data_frame().to_string(columns={self.get_parameter_list()}, "
                     f"index=False, header=False, formatters={{")
        for key, value in self.get_print_formats().items():
            if key == 'SYTM_01':
                pformat = "'{0}': '{{:>{1}}}'.format".format(key, value)
            else:
                pformat = "'{0}': '{{:>{1}f}}'.format".format(key, value)
            formatter = formatter + pformat
            if key_number < nf - 1:
                formatter = formatter + ", "
                key_number += 1
        formatter = formatter + "})"
        output_data_records_v2 = eval(formatter)
        return output_data_records_v2


if __name__ == "__main__":
    
    records = DataRecords()
    df = pd.DataFrame({"PRES_01":[1,4,7], "TEMP_01":[8,5,2], "PSAL_01":[31.5,32.0,32.5]})
    records.set_data_frame(df)
    print(records.print_object())
    print(records.print_object_old_style())
