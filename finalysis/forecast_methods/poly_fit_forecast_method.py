import numpy as np
import pandas as pd

from finalysis.forecast_methods.base_forecast_method import BaseForecastMethod


class PolyFitForecastMethod(BaseForecastMethod):
    def __init__(self, key: str, degree: int = 1):
        self._key = key
        self._degree = degree

    def forecast(self, df: pd.DataFrame) -> int | float:
        periods = [i for i in range(len(df.loc[self._key]))]
        values = df.loc[self._key].to_numpy()

        slope, intercept = np.polyfit(periods, values, self._degree)
        next_period = periods[-1] + 1

        return slope * next_period + intercept
