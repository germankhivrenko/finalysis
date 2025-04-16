import pandas as pd
from finalysis.forecast_methods.base_forecast_method import BaseForecastMethod


class FreeCashFlowForecaster:
    def __init__(self, historical: pd.DataFrame, config: dict[str, BaseForecastMethod]) -> None:
        self._historical = historical
        self._combined = historical.copy()
        self._forecasted = pd.DataFrame(index=historical.index)
        self._config = config  # TODO: add validation (check if keys in df match keys in config)

    @property
    def historical(self):
        return self._forecasted

    @property
    def forecasted(self):
        return self._forecasted

    @property
    def combined(self):
        return self._combined

    def forecast_next(self, periods: int = 1) -> None:
        for _ in range(periods):
            next_period_label = self._combined.columns[-1] + pd.DateOffset(years=1)
            next_period_values = []
            for key in self._combined.index:
                method = self._config[key]
                next_period_values.append(method.forecast(self._combined))
            next_period = pd.DataFrame(next_period_values, index=self._combined.index, columns=[next_period_label])

            self._forecasted = pd.concat([self._forecasted, next_period], axis=1)
            self._combined = pd.concat([self._combined, next_period], axis=1)
