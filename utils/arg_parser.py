import dwave.inspector
import sys

from utils.scheduling_plot import plot_operations, plot_matrix
from utils.util import *

def validate_input(request_body):
    required_fields = ["jobs_data", "T", "lagrange"]
    missing_fields = []
    errors = []
    for required_key in required_fields:
        if required_key not in request_body.keys():
                missing_fields.append(required_key)
    if missing_fields:
        errors.append(f"Missing the required fields {missing_fields}")

    if "simulate" in request_body:
        if "dwave_inspector" in request_body and request_body["simulate"] and request_body["dwave_inspector"]:
            errors.append("You cannot run the dwave inspector on a simulation. Please set 'simulate' to False.")
        if "find_lagrange" in request_body and not request_body["simulate"] and request_body["find_lagrange"]:
            errors.append("Not able to automatically find the langrange parameters on the actual QPU. Please set "
                          "'simulate' to True.")
    if not errors:
        return
    return {"errors": errors}

def execute_flags(arguments, response, jobs_data, operation_results, params, Q, M, success=False):
    if arguments["verbose"]:
        print_first_N_responses(response, 10)
    if arguments["dwave_inspector"]:
        dwave.inspector.show(response)
    # Plot chart
    if arguments["plot_solutions"] and success:
        plot_operations(jobs_data, operation_results)
    # Plot QUBO as confusion matrix
    if arguments["show_matrix"]:
        plot_matrix(Q, jobs_data, M)
