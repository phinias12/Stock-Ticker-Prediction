import numpy as np
import pandas as pd
import matplotlib.pyplot as mpl
from sklearn.preprocessing import scale
from matplotlib.figure import Figure
from TFANN import ANNR
import yfinance as yf

class Predict(object):
    def __init__(self, name, interval, hidden, iterations, tolerance):
        self.name = name
        
        # Retreive data
        if interval == "Day":
            hist = yf.Ticker(name).history(period="2y", interval="1d")
        if interval == "Week":
            hist = yf.Ticker(name).history(period="2y", interval="1wk")
        if interval == "Month":
            hist = yf.Ticker(name).history(period="2y", interval="1mo")

        prices = hist["Open"]
        dates = []
        for d in range(len(prices)):
            dates.append(d)

        df = pd.DataFrame(prices)
        df.insert(1, "Dates", dates, True)

        # Scale Data
        self.stock = scale(df)
        self.hidden = hidden
        self.iterations = iterations
        self.tolerance = tolerance
        
    def predictionGraph(self):
        # Selecting prices and dates
        prices = self.stock[:, 0].reshape(-1, 1)
        dates = self.stock[:, 1].reshape(-1, 1)

        # Train and fit
        input = 1
        output = 1

        layers = [('F', self.hidden), ('AF', 'tanh'), ('F', self.hidden), ('AF', 'tanh'), ('F', self.hidden), ('AF', 'tanh'), ('F', output)]
        mlpr = ANNR([input], layers, batchSize = 256, maxIter = self.iterations, tol = self.tolerance, reg = 1e-4, verbose = True)
        holdDays = 5
        totalDays = len(dates)
        mlpr.fit(dates[0:(totalDays-holdDays)], prices[0:(totalDays-holdDays)])

        # Predict
        pricePredict = mlpr.predict(dates)

        # Plot the graph
        fig = Figure()
        axis = fig.add_subplot()
        axis.plot(dates, prices)
        axis.plot(dates, pricePredict, c='#5aa9ab')
        return axis
    

    