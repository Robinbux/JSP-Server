from flask import Flask, render_template
from flask import request

from JSP import optimize_jobs
from utils.arg_parser import validate_input

app = Flask(__name__)


@app.route("/")
def hello():
    return """To optimize the jobs, make a POST request to '/jsp' with a json body looking like this:
    {
        "jobs_data": [  
            [[0, 3], [1, 2]],
            [[0, 2], [2, 1]]
        ],
        "T": 9,
        "lagrange": {
            "eta": 19,
            "alpha": 15,
            "beta": 41
        },
        "show_matrix": true,
        "plot_solutions": true,
        "dwave_inspector": false,
        "simulate": true,
        "find_lagrange": false
    }"""


@app.route('/jsp', methods=['POST'])
def main():
    request_body = request.get_json()
    val = validate_input(request_body)

    if val is not None: return val
    return optimize_jobs(request_body)


if __name__ == "__main__":
    app.run()
