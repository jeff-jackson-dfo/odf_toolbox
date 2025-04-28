import io
import pandas as pd
from odf_toolbox import odfutils
from typing import NoReturn, Self
from pydantic import BaseModel

class DataRecords(BaseModel):
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
    """

    def __init__(self, 
                 data_frame: pd.DataFrame = pd.DataFrame(),
                 parameter_list: list = None,
                 print_formats: dict = None
                 ):
        self.data_frame = data_frame
        self.parameter_list = parameter_list
        self.print_formats = print_formats

    @property
    def data_frame(self) -> pd.DataFrame:
        return self._data_frame

    @data_frame.setter
    def data_frame(self, dataframe: pd.DataFrame) -> NoReturn:
        self._data_frame = dataframe

    @property
    def parameter_list(self) -> list:
        return self._parameter_list

    @parameter_list.setter
    def parameter_list(self, parameters: list) -> NoReturn:
        self._parameter_list = parameters

    @property
    def print_formats(self) -> dict:
        return self._print_formats

    @print_formats.setter
    def print_formats(self, formats: dict) -> NoReturn:
        self._print_formats = formats

    def __len__(self):
        return len(self._data_frame)

    def populate_object(self, parameter_list: list, data_formats: dict, data_lines_list: list) -> Self:
        data_record_list = [odfutils.split_string_with_quotes(s) for s in data_lines_list]
        df = pd.DataFrame(columns=parameter_list, data=data_record_list)
        df = odfutils.convert_dataframe(df)
        if 'SYTM_01' in df.columns:
            df['SYTM_01'] = df['SYTM_01'].apply(lambda x: f"'{x}'")
        self.data_frame = df
        self.parameter_list = parameter_list
        self.print_formats = data_formats
        return self

    def print_object(self) -> str:
        df = self.data_frame
        plist = self.parameter_list
        q_params = [s for s in plist if s.startswith("Q")]
        value = 'int'
        convert_dict = {key: value for key in q_params}
        df = df.astype(convert_dict)
        self.data_frame = df
        buffer = io.StringIO()
        self.data_frame.to_csv(buffer, index=False, sep=",", lineterminator="\n")
        output_data_records_v3 = buffer.getvalue()
        return output_data_records_v3

    def print_object_old_style(self) -> str:
        nf = len(self.print_formats.items())
        key_number = 0
        formatter = (f"self.data_frame.to_string(columns={self.parameter_list}, "
                     f"index=False, header=False, formatters={{")
        for key, value in self.print_formats.items():
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

def main():
    records = DataRecords()
    df = pd.DataFrame({"PRES_01":[1,4,7], "TEMP_01":[8.2,5.6,2.45], "PSAL_01":[31.5,32.0,32.88]})
    records.data_frame = df
    records.parameter_list = ['PRES_01', "TEMP_01", "PSAL_01"]
    records.print_formats = {'PRES_01': '10.1', "TEMP_01": "10.4", "PSAL_01": '10.4'}
    print(records.print_object())
    print(records.print_object_old_style())

if __name__ == "__main__":
    
    main()