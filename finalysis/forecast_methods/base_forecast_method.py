from abc import ABC, abstractmethod

import pandas as pd


class BaseForecastMethod(ABC):
    @abstractmethod
    def forecast(self, df: pd.DataFrame) -> int | float:
        ...

    def __neg__(self):
        return _NegForecastMethod(self)


class _NegForecastMethod(BaseForecastMethod):
    def __init__(self, original_method: BaseForecastMethod) -> None:
        self._original_method = original_method

    def forecast(self, df: pd.DataFrame) -> int | float:
        return -self._original_method.forecast(df)
