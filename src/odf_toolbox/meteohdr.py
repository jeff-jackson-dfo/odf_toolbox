from odf_toolbox import BaseHeader
from odf_toolbox import odfutils
from typing import NoReturn
from pydantic import BaseModel
class MeteoHeader(BaseModel, BaseHeader):

    def __init__(self, 
                 air_temperature: float = BaseHeader.null_value, 
                 atmospheric_pressure: float = BaseHeader.null_value,
                 wind_speed: float = BaseHeader.null_value,
                 wind_direction: float = BaseHeader.null_value,
                 sea_state: int = BaseHeader.null_value,
                 cloud_cover: int = BaseHeader.null_value,
                 ice_thickness: float = BaseHeader.null_value,
                 meteo_comments: list = None
                 ):
        super().__init__()
        self.air_temperature = air_temperature
        self.atmospheric_pressure = atmospheric_pressure
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.sea_state = sea_state
        self.cloud_cover = cloud_cover
        self.ice_thickness = ice_thickness
        self.meteo_comments = meteo_comments if meteo_comments is not None else []

    def log_meteo_message(self, field: str, old_value: str, new_value: str) -> NoReturn:
        message = f"In Meteo Header field {field.upper()} was changed from '{old_value}' to '{new_value}'"
        super().log_message(message)

    @property
    def air_temperature(self) -> float:
        return self._air_temperature

    @air_temperature.setter
    def air_temperature(self, value: float) -> NoReturn:
        self._air_temperature = value

    @property
    def atmospheric_pressure(self):
        return self._atmospheric_pressure

    @atmospheric_pressure.setter
    def atmospheric_pressure(self, value: float) -> NoReturn:
        self._atmospheric_pressure = value

    @property
    def wind_speed(self) -> float:
        return self._wind_speed

    @wind_speed.setter
    def wind_speed(self, value: float) -> NoReturn:
        self._wind_speed = value

    @property
    def wind_direction(self) -> float:
        return self._wind_direction

    @wind_direction.setter
    def wind_direction(self, value: float) -> NoReturn:
        self._wind_direction = value

    @property
    def sea_state(self) -> int:
        return self._sea_state

    @sea_state.setter
    def sea_state(self, value: int) -> NoReturn:
        self._sea_state = value

    @property
    def cloud_cover(self) -> int:
        return self._cloud_cover

    @cloud_cover.setter
    def cloud_cover(self, value: int) -> NoReturn:
        self._cloud_cover = value

    @property
    def ice_thickness(self) -> float:
        return self._ice_thickness

    @ice_thickness.setter
    def ice_thickness(self, value: float) -> NoReturn:
        self._ice_thickness = value

    @property
    def meteo_comments(self) -> list:
        return self._meteo_comments

    @meteo_comments.setter
    def meteo_comments(self, value: list) -> NoReturn:
        self._meteo_comments = value

    def set_meteo_comment(self, meteo_comment: str, comment_number: int = 0) -> NoReturn:
        meteo_comment = meteo_comment.strip("\'")
        number_of_comments = len(self.meteo_comments)
        if comment_number == 0 and number_of_comments >= 0:
            self._meteo_comments.append(meteo_comment)
        elif comment_number <= number_of_comments and number_of_comments > 0:
            self._meteo_comments[comment_number] = meteo_comment
        else:
            raise ValueError("The 'meteo_comment' number does not match the number of METEO_COMMENTS lines.")

    def populate_object(self, meteo_fields: list) -> None:
        for header_line in meteo_fields:
            tokens = header_line.split('=', maxsplit=1)
            meteo_dict = odfutils.list_to_dict(tokens)
            for key, value in meteo_dict.items():
                key = key.strip()
                value = value.strip()
                if value == -99.0:
                    value = BaseHeader.null_value
                match key:
                    case 'AIR_TEMPERATURE':
                        self.air_temperature = float(value)
                    case 'ATMOSPHERIC_PRESSURE':
                        self.atmospheric_pressure = float(value)
                    case 'WIND_SPEED':
                        self.wind_speed = float(value)
                    case 'WIND_DIRECTION':
                        self.wind_direction = float(value)
                    case 'SEA_STATE':
                        self.sea_state = int(float(value))
                    case 'CLOUD_COVER':
                        self.cloud_cover = int(float(value))
                    case 'ICE_THICKNESS':
                        self.ice_thickness = float(value)
                    case 'METEO_COMMENTS':
                        self.meteo_comments = value

    def print_object(self) -> str:
        meteo_header_output = "METEO_HEADER\n"
        if self.air_temperature == BaseHeader.null_value:
            meteo_header_output += f"  AIR_TEMPERATURE = {self.air_temperature}\n"
        else:
            meteo_header_output += f"  AIR_TEMPERATURE = {self.air_temperature:.2f}\n"
        if self.atmospheric_pressure == BaseHeader.null_value:
            meteo_header_output += f"  ATMOSPHERIC_PRESSURE = {self.atmospheric_pressure}\n"
        else:
            meteo_header_output += f"  ATMOSPHERIC_PRESSURE = {self.atmospheric_pressure:.2f}\n"
        if self.wind_speed == BaseHeader.null_value:
            meteo_header_output += f"  WIND_SPEED = {self.wind_speed}\n"
        else:
            meteo_header_output += f"  WIND_SPEED = {self.wind_speed:.2f}\n"
        if self.wind_direction == BaseHeader.null_value:
            meteo_header_output += f"  WIND_DIRECTION = {self.wind_direction}\n"
        else:
            meteo_header_output += f"  WIND_DIRECTION = {self.wind_direction:.2f}\n"
        if self.sea_state == BaseHeader.null_value:
            meteo_header_output += f"  SEA_STATE = {self.sea_state}\n"
        else:
            meteo_header_output += f"  SEA_STATE = {self.sea_state:.0f}\n"
        if self.cloud_cover == BaseHeader.null_value:
            meteo_header_output += f"  CLOUD_COVER = {self.cloud_cover}\n"
        else:
            meteo_header_output += f"  CLOUD_COVER = {self.cloud_cover:.0f}\n"
        if self.cloud_cover == BaseHeader.null_value:
            meteo_header_output += f"  ICE_THICKNESS = {self.ice_thickness}\n"
        else:
            meteo_header_output += f"  ICE_THICKNESS = {self.ice_thickness:.3f}\n"
        if self.meteo_comments:
            for meteo_comment in self.meteo_comments:
                meteo_header_output += f"  METEO_COMMENTS =  '{meteo_comment}'\n"
        else:
            meteo_header_output += f"  METEO_COMMENTS =  ''\n"
        return meteo_header_output

    @staticmethod
    # Function to convert wind speed from knots to meters per second
    def wind_speed_knots_to_ms(wsKnots) -> float:
        if wsKnots < 0:
            wsMS = -99
        else:
            wsMS = wsKnots / 1.94384
        return wsMS

    @staticmethod
    # Function to covert percentage of cloud cover to the appropriate WMO 2700 code
    def cloud_cover_percentage_to_wmo_code(cloud_cover_percentage: float) -> int:
        cloud_cover_code = None
        if cloud_cover_percentage < 0.0:
           cloud_cover_code = BaseHeader.null_value
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
        return cloud_cover_code

    @staticmethod
    # Function to covert wave height in meters to the appropriate WMO 3700 code
    def wave_height_meters_to_wmo_code(wave_height_meters: float) -> int:
        wave_code = None
        if wave_height_meters < 0.0:
            wave_code = BaseHeader.null_value
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
        return wave_code

def main():
    meteo = MeteoHeader()
    print(meteo.print_object())
    meteo.air_temperature = 10.0
    meteo.atmospheric_pressure = 1000.0
    meteo.wind_speed = meteo.wind_speed_knots_to_ms(5.0)
    meteo.wind_direction = 180.0
    meteo.sea_state = meteo.wave_height_meters_to_wmo_code(3.0)
    meteo.cloud_cover = meteo.cloud_cover_percentage_to_wmo_code(50.0)
    meteo.ice_thickness = 0.0
    meteo.set_meteo_comment("This is a comment")
    print(meteo.print_object())


if __name__ == "__main__":
    main()
