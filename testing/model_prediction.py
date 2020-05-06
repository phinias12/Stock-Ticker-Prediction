from model import Predict

stocks = Predict('FB', 'Day', 200, 2000, 0.075)

figure = stocks.predictionGraph()

# figure.show()