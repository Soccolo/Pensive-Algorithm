# region imports
from AlgorithmImports import *
from f_score import *
# endregion

class FScoreUniverseSelectionModel(FineFundamentalUniverseSelectionModel):

    def __init__(self, algorithm, fscore_threshold):
        super().__init__(self.SelectCoarse, self.SelectFine)
        self.algorithm = algorithm
        self.fscore_threshold = fscore_threshold

    def SelectCoarse(self, coarse):
        '''Defines the coarse fundamental selection function.
        Args:
            algorithm: The algorithm instance
            coarse: The coarse fundamental data used to perform filtering
        Returns:
            An enumerable of symbols passing the filter'''
        # We only want stocks with fundamental data and price > $1
        filtered = [x.Symbol for x in coarse if x.HasFundamentalData and x.Price > 1]
        return filtered

    def SelectFine(self, fine):
        '''Defines the fine fundamental selection function.
        Args:
            algorithm: The algorithm instance
            fine: The fine fundamental data used to perform filtering
        Returns:
            An enumerable of symbols passing the filter'''
        # We use a dictionary to hold the F-Score of each stock
        f_scores = {}

        for f in fine:
            # Calculate the Piotroski F-Score of the given stock
            f_scores[f.Symbol] = self.GetPiotroskiFScore(f)
            if f_scores[f.Symbol] >= self.fscore_threshold:
                self.algorithm.Log(f"Stock: {f.Symbol.ID} :: F-Score: {f_scores[f.Symbol]}")

        # Select the stocks with F-Score higher than the threshold
        selected = [symbol for symbol, fscore in f_scores.items() if fscore >= self.fscore_threshold]

        return selected

    def GetPiotroskiFScore(self, fine):
        '''A helper function to calculate the Piotroski F-Score of a stock
        Arg:
            fine: MorningStar fine fundamental data of the stock
        return:
            the Piotroski F-Score of the stock
        '''
        # initial F-Score as 0
        fscore = 0
        # Add up the sub-scores in different aspects
        fscore += GetROAScore(fine)
        fscore += GetOperatingCashFlowScore(fine)
        fscore += GetROAChangeScore(fine)
        fscore += GetAccrualsScore(fine)
        fscore += GetLeverageScore(fine)
        fscore += GetLiquidityScore(fine)
        fscore += GetShareIssuedScore(fine)
        fscore += GetGrossMarginScore(fine)
        fscore += GetAssetTurnoverScore(fine)
        return fscore
