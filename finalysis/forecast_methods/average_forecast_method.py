import pandas as pd

from finalysis.forecast_methods.base_forecast_method import BaseForecastMethod



class AverageForecastMethod(BaseForecastMethod):
    def __init__(self, key: str) -> None:
        self._key = key

    def forecast(self, df: pd.DataFrame) -> int | float:
        return df.loc[self._key].mean()
