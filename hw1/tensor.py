from typing import Union, List, Tuple, Any

class Tensor:
    def __init__(self, dimension: Union[int, Tuple[int, ...]], values: List[Any]) -> None:
        self.dimension = dimension
        self.values = values

    def __repr__(self) -> str:
        return str(self.values)