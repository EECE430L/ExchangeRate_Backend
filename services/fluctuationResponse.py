import json


class FluctuationResponse:
    def __init__(self, StartDate, usdToLbpRate, lbpToUsdRate):
        self.StartDate = StartDate
        self.usdToLbpRate = usdToLbpRate
        self.lbpToUsdRate = lbpToUsdRate

    def serialize(self):
        return {"Date": self.StartDate, "usdToLbpRate": self.usdToLbpRate, "lbpToUsdRate": self.lbpToUsdRate}
