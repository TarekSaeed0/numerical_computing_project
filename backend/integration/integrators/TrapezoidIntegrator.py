import time
from decimal import Decimal
from typing import Callable

from integration.integrator import Integrator
from integration.result import Result


class TrapezoidIntegrator(Integrator):
    second_derivative: Callable[[Decimal], Decimal]

    def __init__(
        self,
        function: Callable[[Decimal], Decimal],
        lower_limit: Decimal,
        upper_limit: Decimal,
        number_of_subintervals: int,
        precision: int,
        second_derivative: Callable[[Decimal], Decimal],
    ):
        super().__init__(
            function, lower_limit, upper_limit, number_of_subintervals, precision
        )
        self.second_derivative = second_derivative

    def integrate(self) -> Result:
        start_time = time.time()

        value = (
            self.h
            * (
                self.points[0]
                + Decimal("2") * sum(x for x in self.points[1:-1])
                + self.points[-1]
            )
            / Decimal("2")
        )

        maximum_second_derivative = None
        for i in range(self.number_of_subintervals + 1):
            try:
                x = abs(self.second_derivative(self.lower_limit + i * self.h))
                if maximum_second_derivative is None or x > maximum_second_derivative:
                    maximum_second_derivative = x
            except ValueError:
                pass

        absolute_error = None
        if maximum_second_derivative is not None:
            absolute_error = (
                (self.upper_limit - self.lower_limit) ** 3
                / (Decimal("12") * Decimal(self.number_of_subintervals**2))
            ) * maximum_second_derivative

        return Result(
            value=value,
            absolute_error=absolute_error,
            execution_time=time.time() - start_time,
            message="Integration completed using Trapezoid Rule.",
        )
