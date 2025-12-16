from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy
from sympy import real_root
from exceptions import ValidationError
from integration.integrator_factory import IntegratorFactory
from validator import LinearSystemValidator
from equations_solver.solver_factory import SolverFactory
from root_finder.finder_factory import FinderFactory
from decimal import MAX_EMAX, MIN_EMIN, Decimal, getcontext
import signal
import os

app = Flask(__name__)
CORS(app)


@app.route("/api/solve-equations", methods=["POST"])
def solve_equations():
    """Main endpoint to solve linear system or nonlinear equation"""
    try:
        data = request.get_json()

        # Debug logging
        print("\n" + "=" * 50)
        print("Received request:")
        print(f"Data: {data}")

        # Extract data
        method = data.get("method")
        precision = data.get("precision", 6)
        parameters = data.get("parameters", {})

        print(f"method: {method}")
        print(f"precision: {precision}")
        print(f"params: {parameters}")

        # set precision for Decimal operations
        getcontext().prec = precision

        # Validate required fields
        if not method:
            return jsonify({"error": "Missing required field: method"}), 400

        A = data.get("A")
        b = data.get("b")

        print(f"A: {A}")
        print(f"b: {b}")

        if not all([A, b]):
            return jsonify(
                {
                    "error": "Missing required fields: A and b are required for linear system methods"
                }
            ), 400

        A = [[+Decimal(x) for x in y] for y in A]
        b = [+Decimal(x) for x in b]

        # Validate system
        A_matrix, b_vector = LinearSystemValidator.validate_system(A, b)
        precision_value = LinearSystemValidator.validate_precision(precision)

        # Create and run solver
        solver = SolverFactory.create_solver(
            method, A_matrix, b_vector, precision_value, parameters
        )

        result = solver.solve()
        print("=" * 50 + "\n")
        return jsonify(result.to_dict()), 200

    except ValidationError as e:
        print(f"\n Validation Error: {str(e)}\n")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"\n Exception occurred: {str(e)}")
        import traceback

        print("Full traceback:")
        traceback.print_exc()
        print("\n")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/find-root", methods=["POST"])
def find_root():
    try:
        data = request.get_json()

        # Debug logging
        print("\n" + "=" * 50)
        print("Received request:")
        print(f"Data: {data}")

        # Extract data
        function = data.get("function")
        method = data.get("method")
        absolute_relative_error = data.get("absolute_relative_error", "0.00001")
        number_of_iterations = data.get("number_of_iterations", 50)
        precision = data.get("precision", 6)
        parameters = data.get("parameters", {})

        print(f"method: {method}")
        print(f"precision: {precision}")
        print(f"params: {parameters}")

        # set precision for Decimal operations
        getcontext().prec = precision

        # Validate required fields
        if not method:
            return jsonify({"error": "Missing required field: method"}), 400

        if not all([function]):
            return jsonify(
                {"error": "Missing required fields: function for root finding methods"}
            ), 400

        precision_value = LinearSystemValidator.validate_precision(precision)

        # Create and run finder
        finder = FinderFactory.create_finder(
            function=function,
            method=method,
            absolute_relative_error=Decimal(absolute_relative_error),
            number_of_iterations=number_of_iterations,
            precision=precision_value,
            parameters=parameters,
        )

        result = finder.find()
        print("=" * 50 + "\n")
        return jsonify(result.to_dict()), 200

    except ValidationError as e:
        print(f"\n Validation Error: {str(e)}\n")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"\n Exception occurred: {str(e)}")
        import traceback

        print("Full traceback:")
        traceback.print_exc()
        print("\n")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/integrate", methods=["POST"])
def integrate():
    try:
        data = request.get_json()

        # Debug logging
        print("\n" + "=" * 50)
        print("Received request:")
        print(f"Data: {data}")

        # Extract data
        function = data.get("function")
        method = data.get("method")
        lower_limit = data.get("lower_limit")
        upper_limit = data.get("upper_limit")
        number_of_subintervals = data.get("number_of_subintervals", 100)
        precision = data.get("precision", 6)

        print(f"method: {method}")
        print(f"precision: {precision}")

        # set precision for Decimal operations
        getcontext().prec = precision

        # Validate required fields
        if not method:
            return jsonify({"error": "Missing required field: method"}), 400

        if not all([function]):
            return jsonify(
                {"error": "Missing required fields: function for integration methods"}
            ), 400

        if not all([lower_limit, upper_limit]):
            return jsonify(
                {
                    "error": "Missing required fields: lower_limit, upper_limit for integration methods"
                }
            ), 400

        precision_value = LinearSystemValidator.validate_precision(precision)

        # Create and run integrator
        integrator = IntegratorFactory.create_integrator(
            function=function,
            method=method,
            lower_limit=Decimal(lower_limit),
            upper_limit=Decimal(upper_limit),
            number_of_subintervals=number_of_subintervals,
            precision=precision_value,
        )

        result = integrator.integrate()
        print("=" * 50 + "\n")
        return jsonify(result.to_dict()), 200

    except ValidationError as e:
        print(f"\n Validation Error: {str(e)}\n")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"\n Exception occurred: {str(e)}")
        import traceback

        print("Full traceback:")
        traceback.print_exc()
        print("\n")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/methods", methods=["GET"])
def get_methods():
    """Get list of available methods and their parameters"""
    methods = {
        "gauss-elimination": {
            "name": "Gauss Elimination",
            "type": "linear",
            "parameters": [
                {
                    "name": "scaling",
                    "type": "boolean",
                    "default": False,
                    "required": False,
                }
            ],
        },
        "gauss-jordan-elimination": {
            "name": "Gauss-Jordan Elimination",
            "type": "linear",
            "parameters": [
                {
                    "name": "scaling",
                    "type": "boolean",
                    "default": False,
                    "required": False,
                }
            ],
        },
        "lu-decomposition": {
            "name": "LU Decomposition",
            "type": "linear",
            "parameters": [
                {
                    "name": "format",
                    "type": "select",
                    "options": ["doolittle", "crout", "cholesky"],
                    "default": "doolittle",
                    "required": True,
                }
            ],
        },
        "jacobi-iteration": {
            "name": "Jacobi Iteration",
            "type": "linear",
            "parameters": [
                {
                    "name": "initial_guess",
                    "type": "array",
                    "required": False,
                    "description": "Initial guess for solution (defaults to zeros)",
                },
                {
                    "name": "number_of_iterations",
                    "type": "integer",
                    "default": 100,
                    "required": True,
                },
                {
                    "name": "absolute_relative_error",
                    "type": "float",
                    "default": 1e-6,
                    "required": True,
                },
            ],
        },
        "gauss-seidel-iteration": {
            "name": "Gauss-Seidel Iteration",
            "type": "linear",
            "parameters": [
                {
                    "name": "initial_guess",
                    "type": "array",
                    "required": False,
                    "description": "Initial guess for solution (defaults to zeros)",
                },
                {
                    "name": "number_of_iterations",
                    "type": "integer",
                    "default": 100,
                    "required": True,
                },
                {
                    "name": "absolute_relative_error",
                    "type": "float",
                    "default": 1e-6,
                    "required": True,
                },
            ],
        },
        "bisection": {
            "name": "Bisection Method",
            "type": "nonlinear",
            "parameters": [
                {
                    "name": "function",
                    "type": "string",
                    "required": True,
                    "description": "Function expression (e.g., 'x**2 - 2' or 'x**3 - x - 1')",
                },
                {
                    "name": "xl",
                    "type": "float",
                    "required": True,
                    "description": "Lower bound of interval",
                },
                {
                    "name": "xu",
                    "type": "float",
                    "required": True,
                    "description": "Upper bound of interval",
                },
                {
                    "name": "absolute_relative_error",
                    "type": "float",
                    "default": 1e-6,
                    "required": False,
                    "description": "Convergence tolerance",
                },
                {
                    "name": "max_iterations",
                    "type": "integer",
                    "default": 100,
                    "required": False,
                    "description": "Maximum number of iterations",
                },
            ],
        },
        "false-position": {
            "name": "False Position Method",
            "type": "nonlinear",
            "parameters": [
                {
                    "name": "function",
                    "type": "string",
                    "required": True,
                    "description": "Function expression (e.g., 'x**2 - 2' or 'x**3 - x - 1')",
                },
                {
                    "name": "xl",
                    "type": "float",
                    "required": True,
                    "description": "Lower bound of interval",
                },
                {
                    "name": "xu",
                    "type": "float",
                    "required": True,
                    "description": "Upper bound of interval",
                },
                {
                    "name": "absolute_relative_error",
                    "type": "float",
                    "default": 1e-6,
                    "required": False,
                    "description": "Convergence tolerance",
                },
                {
                    "name": "max_iterations",
                    "type": "integer",
                    "default": 100,
                    "required": False,
                    "description": "Maximum number of iterations",
                },
            ],
        },
        "secant": {
            "name": "Secant Method",
            "type": "nonlinear",
            "parameters": [
                {
                    "name": "function",
                    "type": "string",
                    "required": True,
                    "description": "Function expression (e.g., 'x**2 - 2')",
                },
                {
                    "name": "x0",
                    "type": "float",
                    "required": True,
                    "description": "First initial guess (x_i-1)",
                },
                {
                    "name": "x1",
                    "type": "float",
                    "required": True,
                    "description": "Second initial guess (x_i)",
                },
                {
                    "name": "absolute_relative_error",
                    "type": "float",
                    "default": 1e-6,
                    "required": False,
                    "description": "Convergence tolerance",
                },
                {
                    "name": "max_iterations",
                    "type": "integer",
                    "default": 100,
                    "required": False,
                    "description": "Maximum number of iterations",
                },
            ],
        },
        "fixed-point": {
            "name": "Fixed Point Method",
            "type": "nonlinear",
            "parameters": [
                {
                    "name": "function",
                    "type": "string",
                    "required": True,
                    "description": "Function expression (e.g., 'cos(x)' or '(x + 2) ** (1/3)')",
                },
                {
                    "name": "guess",
                    "type": "float",
                    "required": True,
                    "description": "Initial guess for the root",
                },
                {
                    "name": "absolute_relative_error",
                    "type": "float",
                    "default": 1e-6,
                    "required": False,
                    "description": "Convergence tolerance",
                },
                {
                    "name": "max_iterations",
                    "type": "integer",
                    "default": 50,
                    "required": False,
                    "description": "Maximum number of iterations",
                },
            ],
        },
        "newton-raphson": {
            "name": "Newton Raphson Method",
            "type": "nonlinear",
            "parameters": [
                {
                    "name": "function",
                    "type": "string",
                    "required": True,
                    "description": "Function expression (e.g., 'cos(x)' or '(x + 2) ** (1/3)')",
                },
                {
                    "name": "guess",
                    "type": "float",
                    "required": True,
                    "description": "Initial guess for the root",
                },
                {
                    "name": "absolute_relative_error",
                    "type": "float",
                    "default": 1e-6,
                    "required": False,
                    "description": "Convergence tolerance",
                },
                {
                    "name": "max_iterations",
                    "type": "integer",
                    "default": 50,
                    "required": False,
                    "description": "Maximum number of iterations",
                },
                {
                    "name": "m -> multiplicity factor",
                    "type": "integer",
                    "default": 1,
                    "required": False,
                    "description": "Indicates the multiplicity of the root",
                },
            ],
        },
    }
    return jsonify(methods), 200


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {"status": "healthy", "message": "Numerical Methods Solver API"}
    ), 200


@app.route("/shutdown", methods=["POST"])
def shutdown():
    """Gracefully stop the Flask server."""
    os.kill(os.getpid(), signal.SIGTERM)
    return jsonify({"status": "shutting down"})


if __name__ == "__main__":
    getcontext().rounding = "ROUND_HALF_UP"
    getcontext().Emax = MAX_EMAX
    getcontext().Emin = MIN_EMIN

    sympy.cbrt = lambda x: real_root(x, 3)

    app.run(host="0.0.0.0", port=5000, debug=True)
