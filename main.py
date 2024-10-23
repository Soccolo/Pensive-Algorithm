# region imports
from AlgorithmImports import *
from security_initializer import CustomSecurityInitializer
from universe import FScoreUniverseSelectionModel
# endregion

class PensiveFluorescentYellowParrot(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2008, 1, 1)  # Set Start Date
        self.SetEndDate(2024, 10, 19)  # Set End Date
        self.SetCash(30000)  # Set Strategy Cash

        ### Parameters ###
        # The Piotroski F-Score threshold we would like to invest into stocks with F-Score >= of that
        fscore_threshold = self.GetParameter("fscore_threshold", 7)

        ### Reality Modeling ###
        # Interactive Broker Brokerage fees and margin
        self.SetBrokerageModel(BrokerageName.ALPACA, AccountType.MARGIN) #(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)
        # Custom security initializer
        self.SetSecurityInitializer(CustomSecurityInitializer(self.BrokerageModel, FuncSecuritySeeder(self.GetLastKnownPrices)))

        ### Universe Settings ###
        self.UniverseSettings.Resolution = Resolution.Minute

        # Our universe is selected by Piotroski's F-Score
        self.AddUniverseSelection(FScoreUniverseSelectionModel(self, fscore_threshold))
        self.UniverseSettings.Leverage = 2

        # Assume we want to just buy and hold the selected stocks, rebalance daily
        self.AddAlpha(ConstantAlphaModel(InsightType.Price, InsightDirection.Up, timedelta(5)))

        # Avoid overconcentration of risk in related stocks in the same sector, we invest the same size in every sector
        self.SetPortfolioConstruction(SectorWeightingPortfolioConstructionModel())

        # Avoid placing orders with big bid-ask spread to reduce friction cost
        self.SetExecution(SpreadExecutionModel(0.005))  # maximum 1% spread allowed

        # Assume we do not have any risk management measures
        self.add_risk_management(NullRiskManagementModel()) #self.AddRiskManagement(NullRiskManagementModel())

        # Add SPY and set initial investment
        self.spy = self.AddEquity("SPY", Resolution.Minute)
        self.spy.SetLeverage(2)

        #Add GLD for risk management
        self.gld = self.AddEquity("GLD", Resolution.Minute)
        self.gld.SetLeverage(2)

        #Add VIXY for risk management and hedging
        self.vixy = self.AddEquity("VIXY", Resolution.Minute)
        self.vixy.SetLeverage(1)

        # Invest a third of the initial cash into SPY and VIXY
        self.SetHoldings(self.spy.Symbol, 0.35)
        self.SetHoldings(self.gld.Symbol, 0.15)
        self.SetHoldings(self.vixy.Symbol, 0.02)

    def OnData(self, data):
        if not data.ContainsKey(self.spy.Symbol):
            return
        
        # Rebalance SPY to 33% of total portfolio value if not already
        self.SetHoldings(self.spy.Symbol, 0.35)
        self.SetHoldings(self.gld.Symbol, 0.15)
        self.SetHoldings(self.vixy.Symbol, 0.02)
        
        self.Plot("Benchmark", "SPY", self.spy.Price)

    def OnSecuritiesChanged(self, changes):
        # Log the universe changes to test the universe selection model
        # In this case, the added security should be the same as the logged stocks with F-score >= 7
        self.Log(changes)
