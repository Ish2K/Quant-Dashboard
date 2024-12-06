'''
financials = {
        "net_income": net_income,
        "operating_cash_flow": operating_cash_flow,
        "roa_current": roa_current,
        "roa_previous": roa_previous,
        "leverage_current": leverage_current,
        "leverage_previous": leverage_previous,
        "current_ratio_current": current_ratio_current,
        "current_ratio_previous": current_ratio_previous,
        "shares_outstanding_current": shares_outstanding,
        "shares_outstanding_previous": shares_outstanding,  # Assuming no dilution data from yfinance
        "gross_margin_current": gross_margin_current,
        "gross_margin_previous": gross_margin_previous,
        "asset_turnover_current": asset_turnover_current,
        "asset_turnover_previous": asset_turnover_previous,
        "PE Ratio": pe_ratio,
        "PB Ratio": pb_ratio,
        "PS Ratio": ps_ratio,
        "EV to EBITDA": ev_to_ebitda,
        "EV to Sales": ev_to_sales,
        "EV to EBIT": ev_to_ebit,
        "Earnings Per Share": earnings_per_share,
        "Dividend Yield": dividend_yield,
        "Quick Ratio": quick_ratio,
        "Current Ratio": current_ratio,
        "Debt to Equity": debt_to_equity
    }
'''

fundamental_columns = ["net_income", "operating_cash_flow", "roa_current", "roa_previous", "leverage_current", "leverage_previous", "current_ratio_current", "current_ratio_previous", "shares_outstanding_current", "shares_outstanding_previous", "gross_margin_current", "gross_margin_previous", "asset_turnover_current", "asset_turnover_previous", "PE Ratio", "PB Ratio", "PS Ratio", "EV to EBITDA", "EV to Sales", "EV to EBIT", "Earnings Per Share", "Dividend Yield", "Quick Ratio", "Current Ratio", "Debt to Equity"]