from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from icecream import ic
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

    def log_message(self, message):
        super().log_message(f"In Meteo Header field {message}")

    def get_air_temperature(self) -> float:
        return self._air_temperature

    def set_air_temperature(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f'AIR_TEMPERATURE was changed from "{self._air_temperature}" to "{value}"')
        self._air_temperature = value

    def get_atmospheric_pressure(self):
        return self._atmospheric_pressure

    def set_atmospheric_pressure(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f'ATMOSPHERIC_PRESSURE was changed from "{self._atmospheric_pressure}" to "{value}"')
        self._atmospheric_pressure = value

    def get_wind_speed(self) -> float:
        return self._wind_speed

    def set_wind_speed(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f'WIND_SPEED was changed from "{self._wind_speed}" to "{value}"')
        self._wind_speed = value

    def get_wind_direction(self) -> float:
        return self._wind_direction

    def set_wind_direction(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f'WIND_DIRECTION was changed from "{self._wind_direction}" to "{value}"')
        self._wind_direction = value

    def get_sea_state(self) -> float:
        return self._sea_state

    def set_sea_state(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f'SEA_STATE was changed from "{self._sea_state}" to "{value}"')
        self._sea_state = value

    def get_cloud_cover(self) -> float:
        return self._cloud_cover

    def set_cloud_cover(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f'CLOUD_COVER was changed from "{self._cloud_cover}" to "{value}"')
        self._cloud_cover = value

    def get_ice_thickness(self) -> float:
        return self._ice_thickness

    def set_ice_thickness(self, value: float, read_operation: bool = False) -> None:
        value = float(value)
        assert isinstance(value, float), \
               f"Input value is not of type float: {value}"
        if not read_operation:
            self.log_message(f'ICE_THICKNESS was changed from "{self._ice_thickness}" to "{value}"')
        self._ice_thickness = value

    def get_meteo_comments(self) -> list:
        return self._meteo_comments

    def set_meteo_comments(self, meteo_comment: str, comment_number: int = 0, read_operation: bool = False) -> None:
        assert isinstance(meteo_comment, str), \
               f"Input value is not of type str: {meteo_comment}"
        assert isinstance(comment_number, int), \
               f"Input value is not of type int: {comment_number}"
        meteo_comment = meteo_comment.strip("\'")
        number_of_comments = len(self.get_meteo_comments())
        if comment_number == 0 and number_of_comments >= 0:
            if not read_operation:
                self.log_message(f"The following comment was added to METEO_COMMENTS: "
                                     f"'{meteo_comment}'")
                self._meteo_comments.append(meteo_comment)
            else:
                self._meteo_comments.append(meteo_comment)
        elif comment_number <= number_of_comments and number_of_comments > 0:
            if not read_operation:
                self.log_message(f'Comment {comment_number} in METEO_COMMENTS was changed from '
                                     f'"{self._meteo_comments[comment_number-1]}" to "{meteo_comment}"')
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
                                "{:.2f}".format(odfutils.check_float(self.get_air_temperature())) + "\n")
        meteo_header_output += ("  ATMOSPHERIC_PRESSURE = " +
                                "{:.2f}".format(odfutils.check_float(self.get_atmospheric_pressure())) + "\n")
        meteo_header_output += ("  WIND_SPEED = " +
                                "{:.2f}".format(odfutils.check_float(self.get_wind_speed())) + "\n")
        meteo_header_output += ("  WIND_DIRECTION = " +
                                "{:.2f}".format(odfutils.check_float(self.get_wind_direction())) + "\n")
        meteo_header_output += ("  SEA_STATE = " +
                                "{:.0f}".format(odfutils.check_float(self.get_sea_state())) + "\n")
        meteo_header_output += ("  CLOUD_COVER = " +
                                "{:.0f}".format(odfutils.check_float(self.get_cloud_cover())) + "\n")
        meteo_header_output += (
                    "  ICE_THICKNESS = " + "{:.3f}".format(odfutils.check_float(self.get_ice_thickness()))
                    + "\n")
        for meteo_comment in self.get_meteo_comments():
            meteo_header_output += f"  METEO_COMMENTS =  '{meteo_comment}'\n"
        return meteo_header_output

    # Function to convert wind speed from knots to meters per second
    def wind_speed_knots_to_ms(self, wsKnots) -> float:
        if wsKnots < 0:
            wsMS = -99
        else:
            wsMS = wsKnots / 1.94384
        return wsMS

    # Function to covert percentage of cloud cover to the appropriate WMO 2700 code
    def cloud_cover_percentage_to_wmo_code(self, cloud_cover_percentage: float) -> int:
        if cloud_cover_percentage < 0.0:
           cloud_cover_code = -99.0
        elif cloud_cover_percentage == 0.0:
            cloud_cover_code = 0
        elif cloud_cover_percentage > 0.0 and cloud_cover_percentage < 0.15:
           cloud_cover_code = 1
        elif cloud_cover_percentage >= 0.15 and cloud_cover_percentage < 0.35:
            cloud_cover_code = 2
        elif cloud_cover_percentage >= 0.35 and cloud_cover_percentage < 0.45:
            cloud_cover_code = 3
        elif cloud_cover_percentage >= 0.45 and cloud_cover_percentage < 0.55:
            cloud_cover_code = 4
        elif cloud_cover_percentage >= 0.55 and cloud_cover_percentage < 0.65:
            cloud_cover_code = 5
        elif cloud_cover_percentage >= 0.65 and cloud_cover_percentage < 0.85:
            cloud_cover_code = 6
        elif cloud_cover_percentage >= 0.85 and cloud_cover_percentage < 0.95:
            cloud_cover_code = 7
        elif cloud_cover_percentage >= 0.95:
            cloud_cover_code = 8
        elif cloud_cover_percentage >= 1.0:
            cloud_cover_code = 9
        return(cloud_cover_code)

    # Function to covert wave height in meters to the appropriate WMO 3700 code
    def wave_height_meters_to_wmo_code(self, wave_height_meters: float) -> int:
        if wave_height_meters < 0.0:
            wind_speed_knots_to_ms = -99.0
        elif wave_height_meters == 0.0:
            wave_code = 0
        elif wave_height_meters > 0.0 and wave_height_meters < 0.1:
            wave_code = 1
        elif wave_height_meters >= 0.1 and wave_height_meters < 0.5:
            wave_code = 2
        elif wave_height_meters >= 0.5 and wave_height_meters < 1.25:
            wave_code = 3
        elif wave_height_meters >= 1.25 and wave_height_meters < 2.5:
            wave_code = 4
        elif wave_height_meters >= 2.5 and wave_height_meters < 4.0:
            wave_code = 5
        elif wave_height_meters >= 4.0 and wave_height_meters < 6.0:
            wave_code = 6
        elif wave_height_meters >= 6.0 and wave_height_meters < 9.0:
            wave_code = 7
        elif wave_height_meters >= 9.0 and wave_height_meters < 14.0:
            wave_code = 8
        elif wave_height_meters > 14.0:
            wave_code = 9
        return(wave_code)


    def main():
        meteo = MeteoHeader()
        meteo.set_air_temperature(10.0)
        meteo.set_atmospheric_pressure(1000.0)
        meteo.set_wind_speed(meteo.wind_speed_knots_to_ms(5.0))
        meteo.set_wind_direction(180.0)
        meteo.set_sea_state(meteo.wave_height_meters_to_wmo_code(3.0))
        meteo.set_cloud_cover(meteo.cloud_cover_percentage_to_wmo_code(50.0))
        meteo.set_ice_thickness(0.0)
        meteo.set_meteo_comments("This is a comment")
        print(meteo.print_object())


if __name__ == "__main__":
    MeteoHeader.main()
