from odf_toolbox.basehdr import BaseHeader
from odf_toolbox import odfutils

class MeteoHeader(BaseHeader):

    def __init__(self):
        super().__init__()
        self._air_temperature = None
        self._atmospheric_pressure = None
        self._wind_speed = None
        self._wind_direction = None
        self._sea_state = None
        self._cloud_cover = None
        self._ice_thickness = None
        self._meteo_comments = []

    def get_air_temperature(self) -> float:
        return self._air_temperature

    def set_air_temperature(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.logger.info(f"Meteo_Header.Air_Temperature changed from {self._air_temperature} to '{value}'")
        self._air_temperature = value

    def get_atmospheric_pressure(self):
        return self._atmospheric_pressure

    def set_atmospheric_pressure(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.logger.info(f"Meteo_Header.Atmospheric_Pressure changed from {self._atmospheric_pressure} "
                                 f"to '{value}'")
        self._atmospheric_pressure = value

    def get_wind_speed(self) -> float:
        return self._wind_speed

    def set_wind_speed(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.logger.info(f"Meteo_Header.Wind_Speed changed from {self._wind_speed} to '{value}'")
        self._wind_speed = value

    def get_wind_direction(self) -> float:
        return self._wind_direction

    def set_wind_direction(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.logger.info(f"Meteo_Header.Wind_Direction changed from {self._wind_direction} to '{value}'")
        self._wind_direction = value

    def get_sea_state(self) -> float:
        return self._sea_state

    def set_sea_state(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.logger.info(f"Meteo_Header.Sea_State changed from {self._sea_state} to '{value}'")
        self._sea_state = value

    def get_cloud_cover(self) -> float:
        return self._cloud_cover

    def set_cloud_cover(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.logger.info(f"Meteo_Header.Cloud_Cover changed from {self._cloud_cover} to '{value}'")
        self._cloud_cover = value

    def get_ice_thickness(self) -> float:
        return self._ice_thickness

    def set_ice_thickness(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.logger.info(f"Meteo_Header.Ice_Thickness changed from {self._ice_thickness} to '{value}'")
        self._ice_thickness = value

    def get_meteo_comments(self) -> list:
        return self._meteo_comments

    def set_meteo_comments(self, meteo_comment: str, comment_number: int = 0, read_operation: bool = False) -> None:
        assert isinstance(meteo_comment, str), \
               f"Input value is not of type str: {meteo_comment}"
        assert isinstance(comment_number, int), \
               f"Input value is not of type int: {comment_number}"
        number_of_comments = len(self.get_meteo_comments())
        if comment_number == 0 and number_of_comments >= 0:
            if not read_operation:
                self.logger.info(f"The following comment was added to Meteo_Header.Meteo_Comments: "
                                     f"'{meteo_comment}'")
                self._meteo_comments.append(meteo_comment)
        elif comment_number <= number_of_comments and number_of_comments > 0:
            if not read_operation:
                self.logger.info(f"Comment {comment_number} in Meteo_Header.Meteo_Comments was changed from "
                                     f"{self._meteo_comments[comment_number-1]} to '{meteo_comment}'")
            self._meteo_comments[comment_number] = meteo_comment
        else:
            raise ValueError("The 'meteo_comment' number does not match the number of METEO_COMMENTS lines.")

    def populate_object(self, meteo_fields: list) -> None:
        assert isinstance(meteo_fields, list), \
               f"Input value is not of type list: {meteo_fields}"
        for header_line in meteo_fields:
            tokens = header_line.split('=', maxsplit=1)
            meteo_dict = odfutils.list_to_dict(tokens)
            for key, value in meteo_dict.items():
                key = key.strip()
                value = value.strip()
                match key:
                    case 'AIR_TEMPERATURE':
                        self.set_air_temperature(value, read_operation=True)
                    case 'ATMOSPHERIC_PRESSURE':
                        self.set_atmospheric_pressure(value, read_operation=True)
                    case 'WIND_SPEED':
                        self.set_wind_speed(value, read_operation=True)
                    case 'WIND_DIRECTION':
                        self.set_wind_direction(value, read_operation=True)
                    case 'SEA_STATE':
                        self.set_sea_state(value, read_operation=True)
                    case 'CLOUD_COVER':
                        self.set_cloud_cover(value, read_operation=True)
                    case 'ICE_THICKNESS':
                        self.set_ice_thickness(value, read_operation=True)
                    case 'METEO_COMMENTS':
                        self.set_meteo_comments(value, read_operation=True)

    def print_object(self) -> str:
        meteo_header_output = "METEO_HEADER\n"
        meteo_header_output += ("  AIR_TEMPERATURE = " +
                                "{:.2f}".format(odfutils.check_float_value(self.get_air_temperature())) + "\n")
        meteo_header_output += ("  ATMOSPHERIC_PRESSURE = " +
                                "{:.2f}".format(odfutils.check_float_value(self.get_atmospheric_pressure())) + "\n")
        meteo_header_output += ("  WIND_SPEED = " +
                                "{:.2f}".format(odfutils.check_float_value(self.get_wind_speed())) + "\n")
        meteo_header_output += ("  WIND_DIRECTION = " +
                                "{:.2f}".format(odfutils.check_float_value(self.get_wind_direction())) + "\n")
        meteo_header_output += ("  SEA_STATE = " +
                                "{:.0f}".format(odfutils.check_float_value(self.get_sea_state())) + "\n")
        meteo_header_output += ("  CLOUD_COVER = " +
                                "{:.0f}".format(odfutils.check_float_value(self.get_cloud_cover())) + "\n")
        meteo_header_output += (
                    "  ICE_THICKNESS = " + "{:.3f}".format(odfutils.check_float_value(self.get_ice_thickness()))
                    + "\n")
        for meteo_comment in self.get_meteo_comments():
            meteo_header_output += f"  METEO_COMMENTS =  {meteo_comment}\n"
        return meteo_header_output
