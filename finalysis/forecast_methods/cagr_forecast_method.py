import pandas as pd
from finalysis.forecast_methods.base_forecast_method import BaseForecastMethod


class CAGRForecastMethod(BaseForecastMethod):
    def __init__(self, key: str) -> None:
        self._key = key

    def forecast(self, df: pd.DataFrame) -> int | float:
        cagr = self._calc_cagr(df)

        return df.loc[self._key].iloc[-1] * (1 + cagr)

    def _calc_cagr(self, df: pd.DataFrame) -> float:
        first = df.loc[self._key].iloc[0]
        last = df.loc[self._key].iloc[-1]
        periods = len(df.loc[self._key]) - 1

        return (last / first) ** (1 / periods) - 1

