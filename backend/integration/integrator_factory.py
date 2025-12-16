from decimal import Decimal, InvalidOperation, Overflow
from validator import FunctionValidator
from exceptions import ValidationError

# Import all finder classes here
from integration.integrators.TrapezoidIntegrator import TrapezoidIntegrator
from integration.integrators.Simpson13Integrator import Simpson13Integrator
from integration.integrators.Simpson38Integrator import Simpson38Integrator
from sympy import Expr, symbols


class IntegratorFactory:
    @staticmethod
    def create_integrator(
        function: str,
        method: str,
        lower_limit: Decimal,
        upper_limit: Decimal,
        number_of_subintervals: int,
        precision: int,
    ):
        f_expr: Expr = FunctionValidator.validate_and_parse(function)

        x_symbol = symbols("x", real=True)

        def f(x):
            val_sympy = f_expr.subs(x_symbol, x).evalf(n=precision, chop=True)

            try:
                if not val_sympy.is_real:
                    raise ValueError(
                        "calculation resulted in undefined or complex value"
                    )
                y = +Decimal(str(val_sympy))
            except (InvalidOperation, ValueError):
                raise ValueError("calculation resulted in undefined or complex value")
            except Overflow:
                raise ValueError("calculation resulted in overflow")

            return y

        if method == "trapezoid":
            ddf_expr = f_expr.diff(x_symbol, 2)

            def ddf(x):
                val_sympy = ddf_expr.subs(x_symbol, x).evalf(n=precision, chop=True)

                try:
                    if not val_sympy.is_real:
                        raise ValueError(
                            "calculation resulted in undefined or complex value"
                        )
                    y = +Decimal(str(val_sympy))
                except (InvalidOperation, ValueError):
                    raise ValueError(
                        "calculation resulted in undefined or complex value"
                    )
                except Overflow:
                    raise ValueError("calculation resulted in overflow")

                return y

            return TrapezoidIntegrator(
                function=f,
                lower_limit=lower_limit,
                upper_limit=upper_limit,
                number_of_subintervals=number_of_subintervals,
                precision=precision,
                second_derivative=ddf,
            )
        elif method == "simpson-1-3" or method == "simpson-3-8":
            d4f_expr = f_expr.diff(x_symbol, 4)

            def d4f(x):
                val_sympy = d4f_expr.subs(x_symbol, x).evalf(n=precision, chop=True)

                try:
                    if not val_sympy.is_real:
                        raise ValueError(
                            "calculation resulted in undefined or complex value"
                        )
                    y = +Decimal(str(val_sympy))
                except (InvalidOperation, ValueError):
                    raise ValueError(
                        "calculation resulted in undefined or complex value"
                    )
                except Overflow:
                    raise ValueError("calculation resulted in overflow")

                return y

            if method == "simpson-1-3":
                return Simpson13Integrator(
                    function=f,
                    lower_limit=lower_limit,
                    upper_limit=upper_limit,
                    number_of_subintervals=number_of_subintervals,
                    precision=precision,
                    fourth_derivative=d4f,
                )
            elif method == "simpson-3-8":
                return Simpson38Integrator(
                    function=f,
                    lower_limit=lower_limit,
                    upper_limit=upper_limit,
                    number_of_subintervals=number_of_subintervals,
                    precision=precision,
                    fourth_derivative=d4f,
                )
        else:
            raise ValidationError(f"Unknown method: {method}")
