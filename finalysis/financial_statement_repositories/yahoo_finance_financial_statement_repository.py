import pandas as pd
from collections.abc import Sequence
from yfinance import Ticker
from finalysis.constants import financial_statement_item_keys as ITEM_KEYS

_ITEM_MAPPING = {
    ITEM_KEYS.REVENUE: "Total Revenue",
    ITEM_KEYS.COST_OF_REVENUE: "Cost Of Revenue",
    ITEM_KEYS.OPERATING_EXPENSE: "Operating Expense",
    ITEM_KEYS.NON_OPERATING_INTEREST_INCOME_EXPENSE: "Net Non Operating Interest Income Expense",
    ITEM_KEYS.OTHER_INCOME_EXPENSE: "Other Income Expense",
    ITEM_KEYS.EARNINGS_FROM_EQUITY_INTEREST_NET: "Earnings From Equity Interest Net Of Tax",
    ITEM_KEYS.PRETAX_INCOME: "Pretax Income",
    ITEM_KEYS.TAX_PROVISION: "Tax Provision",
    ITEM_KEYS.INTEREST_EXPENSE: "Interest Expense",

    ITEM_KEYS.STOCKHOLDERS_EQUITY: "Stockholders Equity",
    ITEM_KEYS.TOTAL_DEBT: "Total Debt",

    ITEM_KEYS.OPERATING_GAINS_LOSSES: "Operating Gains Losses",
    ITEM_KEYS.DEPRECIATION: "Depreciation Amortization Depletion",
    ITEM_KEYS.DEFERRED_TAX: "Deferred Tax",
    ITEM_KEYS.STOCK_BASED_COMPENSATION: "Stock Based Compensation",
    ITEM_KEYS.ASSET_IMPAIRMENT_CHARGE: "Asset Impairment Charge",
    ITEM_KEYS.UNREALIZED_GAIN_LOSS_ON_INVESTMENT: "Unrealized Gain Loss On Investment Securities",
    ITEM_KEYS.OTHER_NON_CASH_ITEMS: "Other Non Cash Items",
    ITEM_KEYS.CAPITAL_EXPENDITURE: "Capital Expenditure",

    ITEM_KEYS.WORKING_CAPITAL_CHANGE: "Change In Working Capital",


    ITEM_KEYS.FREE_CASH_FLOW: "Free Cash Flow",
}


class YahooFinanceFinancialStatementRepository:
    def retrieve(self, ticker: str, items: Sequence[str]) -> pd.DataFrame:
        fin_statement = self._load_fin_statement(ticker)
        return self._map_fin_items(fin_statement, items)

    def _load_fin_statement(self, ticker: str) -> pd.DataFrame:
        ticker = Ticker(ticker)

        return pd.concat([
            ticker.income_stmt,
            ticker.balance_sheet,
            ticker.cash_flow,
        ])

    def _map_fin_items(self, fin_statement: pd.DataFrame, items: Sequence[str]) -> pd.DataFrame:
        output_items = []
        for item in items:
            yfinance_item_key = _ITEM_MAPPING[item]
            if yfinance_item_key in fin_statement.index:
                item_df = (
                    fin_statement
                        .loc[[yfinance_item_key]]
                        .rename(index={yfinance_item_key: item})
                        # .fillna(0)
                        # .infer_objects(copy=False)
                        # .astype(int)
                )
                output_items.append(item_df)

        result = pd.concat(output_items)

        if ITEM_KEYS.REVENUE in result.index:
            return result[result.columns[::-1]].dropna(axis=1, subset=[ITEM_KEYS.REVENUE])

        return result[result.columns[::-1]]
