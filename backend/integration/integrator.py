from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Callable, List

from exceptions import ValidationError
from integration.result import Result


# base class for all integration methods
class Integrator(ABC):
    function: Callable[[Decimal], Decimal]
    lower_limit: Decimal
    upper_limit: Decimal
    number_of_subintervals: int
    precision: int
    h: Decimal
    points: List[Decimal]

    def __init__(
        self,
        function: Callable[[Decimal], Decimal],
        lower_limit: Decimal,
        upper_limit: Decimal,
        number_of_subintervals: int,
        precision: int,
    ):
        if lower_limit > upper_limit:
            raise ValidationError("lower limit must be less than upper limit")

        self.function = function
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.number_of_subintervals = number_of_subintervals
        self.precision = precision
        self.h = (self.upper_limit - self.lower_limit) / Decimal(
            self.number_of_subintervals
        )

        self.points = [
            self.function(self.lower_limit + i * self.h)
            for i in range(self.number_of_subintervals + 1)
        ]

    # integrate the function over an interval
    @abstractmethod
    def integrate(self) -> Result:
        pass
