from typing import Union, List, Tuple, Any
from tensor import Tensor

class Matrix(Tensor):
    def __init__(self, dimension: Tuple[int, int], values: List[Any]) -> None:
        super().__init__(dimension, values)
        self.rows, self.columns = dimension

    def conv_rc2i(self, row: int, column: int) -> int:
        return row * self.columns + column

    def conv_i2rc(self, index: int) -> Tuple[int, int]:
        row = index // self.columns
        column = index % self.columns
        return (row, column)

    def __str__(self) -> str:
        max_value_length: int = max(len(str(item)) for item in self.values)
        matrix_string: str = "["
        for row_index in range(self.rows):
            row = []
            matrix_string += "\n"
            for column in range(self.columns):
                index = self.conv_rc2i(row_index, column)
                value = str(self.values[index]).rjust(max_value_length)
                row.append(value)
            matrix_string += "   " + "  ".join(row) + "\n"
        matrix_string += "]"
        return matrix_string

    def __getitem__(self, key: Union[int, slice, List[int], Tuple[Union[int, list, slice], Union[int, list, slice]]]) -> Any:
        if isinstance(key, tuple) and len(key) == 2 and all(isinstance(key_value, int) for key_value in key):
            return self.values[self.conv_rc2i(*key)]
        elif isinstance(key, int):
            value = [self.values[self.conv_rc2i(key, index)] for index in range(self.columns)]
            return Matrix((1, self.columns), value)
        elif isinstance(key, slice):
            row_indexes = list(range(self.rows)[key])
            value = []
            for row_index in row_indexes:
                row = self.values[row_index * self.columns : (row_index + 1) * self.columns]
                value.extend(row)
            return Matrix((len(row_indexes), self.columns), value)
        elif isinstance(key, list):
            value = []
            for row_index in key:
                row = self.values[row_index * self.columns : (row_index + 1) * self.columns]
                value.extend(row)
            return Matrix((len(key), self.columns), value)
        else:
            row_indexes = self._process_key(key[0], self.rows)
            column_indexes = self._process_key(key[1], self.columns)
            value = []
            for row_index in row_indexes:
                for column_index in column_indexes:
                    value.append(self.values[self.conv_rc2i(row_index, column_index)])
            return Matrix((len(row_indexes), len(column_indexes)), value)

    def _process_key(self, key: Union[int, list, slice], size: int) -> List[int]:
        if isinstance(key, int):
            return [key]
        elif isinstance(key, slice):
            return list(range(size)[key])
        else:
            return key