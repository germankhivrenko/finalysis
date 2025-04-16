import pandas as pd
from typing import Protocol
from collections.abc import Sequence


class FinancialStatementRepository(Protocol):
    def retreive(self, ticker: str, item_keys: Sequence[str]) -> pd.DataFrame:
        ...