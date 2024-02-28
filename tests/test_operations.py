"""
This module contains unit tests for arithmetic operations and Calculation class functionality.

It uses pytest to parameterize tests for various arithmetic operations (addition, subtraction,
multiplication, division), including edge cases like division by zero and invalid inputs.
Tests ensure that the calculation results match expected outcomes and that the appropriate
exceptions are raised for invalid operations.
"""
from decimal import Decimal
import pytest
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide # pylint: disable=unused-import

# pylint: disable=invalid-name
def test_operation(a, b, operation, expected):
    '''Testing various operations'''
    calculation = Calculation.create(a, b, operation)
    assert calculation.perform() == expected, f"{operation.__name__} operation failed"

# Keeping the divide by zero test as is since it tests a specific case
def test_divide_by_zero():
    '''Testing the divide by zero exception'''
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculation = Calculation(Decimal('10'), Decimal('0'), divide)
        calculation.perform()
