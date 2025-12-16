import time
from decimal import Decimal
from typing import Callable

from exceptions import ValidationError
from integration.integrator import Integrator
from integration.result import Result


class Simpson13Integrator(Integrator):
    fourth_derivative: Callable[[Decimal], Decimal]

    def __init__(
        self,
        function: Callable[[Decimal], Decimal],
        lower_limit: Decimal,
        upper_limit: Decimal,
        number_of_subintervals: int,
        precision: int,
        fourth_derivative: Callable[[Decimal], Decimal],
    ):
        super().__init__(
            function, lower_limit, upper_limit, number_of_subintervals, precision
        )

        self.fourth_derivative = fourth_derivative

        if self.number_of_subintervals % 2 != 0:
            raise ValidationError(
                "Number of subintervals must be even for Simpson's 1/3 Rule"
            )

    def integrate(self) -> Result:
        start_time = time.time()

        value = (
            self.h
            * (
                self.points[0]
                + Decimal("4")
                * sum(x for i, x in enumerate(self.points[1:-1]) if (i + 1) % 2 != 0)
                + Decimal("2")
                * sum(x for i, x in enumerate(self.points[1:-1]) if (i + 1) % 2 == 0)
                + self.points[-1]
            )
            / Decimal("3")
        )

        maximum_fourth_derivative = None
        for i in range(self.number_of_subintervals + 1):
            try:
                x = abs(self.fourth_derivative(self.lower_limit + i * self.h))
                if maximum_fourth_derivative is None or x > maximum_fourth_derivative:
                    maximum_fourth_derivative = x
            except ValueError:
                pass

        absolute_error = None
        if maximum_fourth_derivative is not None:
            absolute_error = (
                (self.upper_limit - self.lower_limit) ** 5
                / (Decimal("180") * Decimal(self.number_of_subintervals**4))
            ) * maximum_fourth_derivative

        return Result(
            value=value,
            absolute_error=absolute_error,
            execution_time=time.time() - start_time,
            message="Integration completed using Simpson's 1/3 Rule.",
        )
