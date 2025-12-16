from decimal import Decimal
from typing import Dict, Optional, Any


class Result:
    value: Optional[Decimal]
    absolute_error: Optional[Decimal]
    execution_time: float
    message: str

    def __init__(
        self,
        value: Optional[Decimal] = None,
        absolute_error: Optional[Decimal] = None,
        execution_time: float = 0.0,
        message: str = "Solution found",
    ):
        self.value = value
        self.absolute_error = absolute_error
        self.execution_time = execution_time
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "message": self.message,
            "execution_time": round(self.execution_time, 12),
        }

        if self.value is not None:
            result["value"] = self.value

        if self.absolute_error is not None:
            result["absolute_error"] = self.absolute_error

        return result
