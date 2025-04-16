import pandas as pd
from finalysis.forecast_methods.base_forecast_method import BaseForecastMethod


class PercentageOfForecastMethod(BaseForecastMethod):
    def __init__(self, original_method: BaseForecastMethod, percent: float) -> None:
        self._original_method = original_method
        self._percent = percent

    def forecast(self, df: pd.DataFrame) -> int | float:
        return self._original_method.forecast(df) * self._percent
