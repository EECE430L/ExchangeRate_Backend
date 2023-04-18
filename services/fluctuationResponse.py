import json


class fluctuationResponseUsdToLbp:
    def __init__(self, StartDate, EndDate, usdToLbpRate):
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.usdToLbpRate = usdToLbpRate

    def serialize(self):
        return {"StartDate": self.StartDate, "EndDate": self.EndDate, "usdToLbpRate": self.usdToLbpRate}


class fluctuationResponseLbpToUsd:
    def __init__(self, StartDate, EndDate, lbpToUsdRate):
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.lbpToUsdRate = lbpToUsdRate

    def serialize(self):
        return {"StartDate": self.StartDate, "EndDate": self.EndDate, "lbpToUsdRate": self.lbpToUsdRate}
