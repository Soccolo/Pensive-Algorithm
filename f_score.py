# region imports
from AlgorithmImports import *
# endregion
def GetROAScore(fine):
    '''Get the Profitability - Return of Asset sub-score of Piotroski F-Score
    Arg:
        fine: Fine fundamental object of a stock
    Return:
        Profitability - Return of Asset sub-score'''
    # Nearest ROA as current year data
    roa = fine.OperationRatios.ROA.ThreeMonths
    # 1 score if ROA datum exists and positive, else 0
    score = 1 if roa and roa > 0 else 0
    return score

def GetOperatingCashFlowScore(fine):
    '''Get the Profitability - Operating Cash Flow sub-score of Piotroski F-Score
    Arg:
        fine: Fine fundamental object of a stock
    Return:
        Profitability - Operating Cash Flow sub-score'''
    # Nearest Operating Cash Flow as current year data
    operating_cashflow = fine.FinancialStatements.CashFlowStatement.CashFlowFromContinuingOperatingActivities.ThreeMonths
    # 1 score if operating cash flow datum exists and positive, else 0
    score = 1 if operating_cashflow and operating_cashflow > 0 else 0
    return score

def GetROAChangeScore(fine):
    '''Get the Profitability - Change in Return of Assets sub-score of Piotroski F-Score
    Arg:
        fine: Fine fundamental object of a stock
    Return:
        Profitability - Change in Return of Assets sub-score'''
    # if current or previous year's ROA data does not exist, return 0 score
    roa = fine.OperationRatios.ROA
    if not roa.ThreeMonths or not roa.OneYear:
        return 0

    # 1 score if change in ROA positive, else 0 score
    score = 1 if roa.ThreeMonths > roa.OneYear else 0
    return score

def GetAccrualsScore(fine):
    '''Get the Profitability - Accruals sub-score of Piotroski F-Score
    Arg:
        fine: Fine fundamental object of a stock
    Return:
        Profitability - Accruals sub-score'''
    # Nearest Operating Cash Flow, Total Assets, ROA as current year data
    operating_cashflow = fine.FinancialStatements.CashFlowStatement.CashFlowFromContinuingOperatingActivities.ThreeMonths
    total_assets = fine.FinancialStatements.BalanceSheet.TotalAssets.ThreeMonths
    roa = fine.OperationRatios.ROA.ThreeMonths
    # 1 score if operating cash flow, total assets and ROA exists, and operating cash flow / total assets > ROA, else 0
    score = 1 if operating_cashflow and total_assets and roa and operating_cashflow / total_assets > roa else 0
    return score

def GetLeverageScore(fine):
    '''Get the Leverage, Liquidity and Source of Funds - Change in Leverage sub-score of Piotroski F-Score
    Arg:
        fine: Fine fundamental object of a stock
    Return:
        Leverage, Liquidity and Source of Funds - Change in Leverage sub-score'''
    # if current or previous year's long term debt to equity ratio data does not exist, return 0 score
    long_term_debt_ratio = fine.OperationRatios.LongTermDebtEquityRatio
    if not long_term_debt_ratio.ThreeMonths or not long_term_debt_ratio.OneYear:
        return 0

    # 1 score if long term debt ratio is lower in the current year, else 0 score
    score = 1 if long_term_debt_ratio.ThreeMonths < long_term_debt_ratio.OneYear else 0
    return score

def GetLiquidityScore(fine):
    '''Get the Leverage, Liquidity and Source of Funds - Change in Liquidity sub-score of Piotroski F-Score
    Arg:
        fine: Fine fundamental object of a stock
    Return:
        Leverage, Liquidity and Source of Funds - Change in Liquidity sub-score'''
    # if current or previous year's current ratio data does not exist, return 0 score
    current_ratio = fine.OperationRatios.CurrentRatio
    if not current_ratio.ThreeMonths or not current_ratio.OneYear:
        return 0

    # 1 score if current ratio is higher in the current year, else 0 score
    score = 1 if current_ratio.ThreeMonths > current_ratio.OneYear else 0
    return score

def GetShareIssuedScore(fine):
    '''Get the Leverage, Liquidity and Source of Funds - Change in Number of Shares sub-score of Piotroski F-Score
    Arg:
        fine: Fine fundamental object of a stock
    Return:
        Leverage, Liquidity and Source of Funds - Change in Number of Shares sub-score'''
    # if current or previous year's issued shares data does not exist, return 0 score
    shares_issued = fine.FinancialStatements.BalanceSheet.ShareIssued
    if not shares_issued.ThreeMonths or not shares_issued.TwelveMonths:
        return 0

    # 1 score if shares issued did not increase in the current year, else 0 score
    score = 1 if shares_issued.ThreeMonths <= shares_issued.TwelveMonths else 0
    return score

def GetGrossMarginScore(fine):
    '''Get the Leverage, Liquidity and Source of Funds - Change in Gross Margin sub-score of Piotroski F-Score
    Arg:
        fine: Fine fundamental object of a stock
    Return:
        Leverage, Liquidity and Source of Funds - Change in Gross Margin sub-score'''
    # if current or previous year's gross margin data does not exist, return 0 score
    gross_margin = fine.OperationRatios.GrossMargin
    if not gross_margin.ThreeMonths or not gross_margin.OneYear:
        return 0

    # 1 score if gross margin is higher in the current year, else 0 score
    score = 1 if gross_margin.ThreeMonths > gross_margin.OneYear else 0
    return score

def GetAssetTurnoverScore(fine):
    '''Get the Leverage, Liquidity and Source of Funds - Change in Asset Turnover Ratio sub-score of Piotroski F-Score
    Arg:
        fine: Fine fundamental object of a stock
    Return:
        Leverage, Liquidity and Source of Funds - Change in Asset Turnover Ratio sub-score'''
    # if current or previous year's asset turnover data does not exist, return 0 score
    asset_turnover = fine.OperationRatios.AssetsTurnover
    if not asset_turnover.ThreeMonths or not asset_turnover.OneYear:
        return 0

    # 1 score if asset turnover is higher in the current year, else 0 score
    score = 1 if asset_turnover.ThreeMonths > asset_turnover.OneYear else 0
    return score
