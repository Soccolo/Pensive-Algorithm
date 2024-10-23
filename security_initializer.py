# region imports
from AlgorithmImports import *
# endregion

class CustomSecurityInitializer(BrokerageModelSecurityInitializer):

    def __init__(self, brokerage_model: IBrokerageModel, security_seeder: ISecuritySeeder) -> None:
        super().__init__(brokerage_model, security_seeder)

    def Initialize(self, security: Security) -> None:
        # First, call the superclass definition
        # This method sets the reality models of each security using the default reality models of the brokerage model
        super().Initialize(security)
        
        # We want a slippage model with price impact by order size for reality modeling
        security.SetSlippageModel(VolumeShareSlippageModel())
        security.SetLeverage(2)
