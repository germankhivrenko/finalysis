from yfinance import Ticker
from finalysis.financial_statement_repositories.financial_statement_repository import FinancialStatementRepository
import finalysis.constants.financial_statement_item_keys as ITEM_KEYS


EXPECTED_MARKET_RETURN = 0.1


class WACCCalculator:
    # WACC = (E/V) * Re + (D/V) * Rd * (1 - Tc)
    # Re = Rf + β * (Rm - Rf)
    # Rd = Interest Expense / Total Debt
    # Tax Rate
    def __init__(self, fin_statement_repository: FinancialStatementRepository) -> None:
        self._fin_statement_repository = fin_statement_repository

    def calculate(self, ticker: str) -> float:
        equity_weight = self._get_equity_weight(ticker)
        debt_weight = self._get_debt_weight(ticker)
        cost_of_equity = self._get_cost_of_equity(ticker)
        cost_of_debt = self._get_cost_of_debt(ticker)
        tax_rate = self._get_tax_rate(ticker)

        return float(equity_weight * cost_of_equity + debt_weight * cost_of_debt * (1 - tax_rate))

    def _get_equity_weight(self, ticker: str) -> float:
        equity = self._get_equity(ticker)
        debt = self._get_debt(ticker)

        return equity / (equity + debt)

    def _get_debt_weight(self, ticker: str) -> float:
        equity = self._get_equity(ticker)
        debt = self._get_debt(ticker)

        return debt / (equity + debt)

    def _get_cost_of_equity(self, ticker: str) -> float:
        risk_free_rate = self._get_risk_free_rate()
        beta = self._get_beta(ticker)
        market_return = self._get_market_return()

        return risk_free_rate + beta * (market_return - risk_free_rate)

    def _get_cost_of_debt(self, ticker: str) -> float:
        interest_income_df = self._fin_statement_repository.retrieve(ticker, [ITEM_KEYS.INTEREST_EXPENSE]).infer_objects(copy=False).fillna(0)
        debt = self._get_debt(ticker)

        return interest_income_df.iloc[0].iloc[-1] / debt

    def _get_tax_rate(self, ticker: str) -> float:
        df = self._fin_statement_repository.retrieve(ticker, [
            ITEM_KEYS.PRETAX_INCOME,
            ITEM_KEYS.TAX_PROVISION,
        ]).dropna(axis=1)
        hist_tax_rates = df.loc[ITEM_KEYS.TAX_PROVISION] / df.loc[ITEM_KEYS.PRETAX_INCOME]

        return hist_tax_rates.iloc[-1]

    def _get_equity(self, ticker: str) -> float:
        df = self._fin_statement_repository.retrieve(ticker, [ITEM_KEYS.STOCKHOLDERS_EQUITY])

        return df.iloc[0].iloc[-1]

    def _get_debt(self, ticker: str) -> float:
        df = self._fin_statement_repository.retrieve(ticker, [ITEM_KEYS.TOTAL_DEBT])

        return df.iloc[0].tail(2).mean()

    def _get_beta(self, ticker: str) -> float:
        stock = Ticker(ticker)
        return stock.info['beta']

    def _get_risk_free_rate(self) -> float:
        tnx = Ticker("^TNX")
        hist = tnx.history(period="5d")

        return hist['Close'].iloc[-1] / 100

    def _get_market_return(self) -> float:
        return EXPECTED_MARKET_RETURN
