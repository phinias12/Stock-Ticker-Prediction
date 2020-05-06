import io
from flask import Flask, render_template, Response, request, redirect, url_for
from model import Predict
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


app = Flask(__name__)

@app.route('/home')
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/plot', methods=["GET", "POST"])
def plot():
    if request.method == "POST":
        stock = request.form.get("ticker")
        interval = request.form.get("interval")
        iterations = request.form.get("iterations")
        tolerance = request.form.get("tolerance")
        hidden = request.form.get("layers")
    
        data = Predict(stock, interval, int(hidden), int(iterations), float(tolerance))

        figure = data.predictionGraph()
        output = io.BytesIO()
        FigureCanvas(figure).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    if request.method == "GET":
        return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)