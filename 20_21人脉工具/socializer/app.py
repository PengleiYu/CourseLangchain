from flask import Flask, render_template, request, jsonify

from findbigV import find_big_v

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/process", methods=["POST"])
def process():
    flower_ = request.form['flower']
    response_dict = find_big_v(flower_type=flower_)

    return jsonify(response_dict)


if __name__ == '__main__':
    app.run(debug=True)
