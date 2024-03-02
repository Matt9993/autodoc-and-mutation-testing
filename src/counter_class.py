"""Represent a dummy class to test with"""
from dataclasses import dataclass


@dataclass
class Counter:
    """
    Counter dataclass.

    Fields:
        _value (int): Representing and holding the value of the Counter.
    """
    _value : int = 0


    def add(self, value: int) -> None:
        """
        Increment the current value with the specified number.

        Args:
            value (int): The number to add to the current value.

        Raises:
            TypeError: A TypeError is raised if value is not an integer.
        """
        if isinstance(value, int):
            self._value += value
        else:
            raise TypeError("Value must be of type integer")

    def remove(self, value) -> None:
        """
        Decrease the current value by the specified number.

        Args:
            value (int): The number to extract from the current value.

        Raises:
            TypeError: A TypeError is raised if value is not an integer.
        """
        if isinstance(value, int):
            self._value -= value
        else:
            raise TypeError("Value must be of type integer")

    def clear(self) -> None:
        """
        Restores the Counter objects value to zero.
        """
        self._value = 0
