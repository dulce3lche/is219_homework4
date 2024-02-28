"""
This module contains pytest tests for the calculate_and_print function in the main module.
It tests various scenarios including different arithmetic operations, division by zero,
unknown operations, and invalid number inputs.
"""
import pytest
from main import calculate_and_print  # Ensure this import matches your project structure

@pytest.mark.parametrize("a_string, b_string, operation_string, expected_string", [
    ("5", "3", 'add', "The result of 5 add 3 is equal to 8"),
    ("10", "2", 'subtract', "The result of 10 subtract 2 is equal to 8"),
    ("4", "5", 'multiply', "The result of 4 multiply 5 is equal to 20"),
    ("20", "4", 'divide', "The result of 20 divide 4 is equal to 5"),
    ("1", "0", 'divide', "An error occurred: Cannot divide by zero"),  # Adjusted for the actual error message
    ("9", "3", 'unknown', "Unknown operation: unknown"),  # Test for unknown operation
    ("a", "3", 'add', "Invalid number input: a or 3 is not a valid number."),  # Testing invalid number input
    ("5", "b", 'subtract', "Invalid number input: 5 or b is not a valid number.")  # Testing another invalid number input
])
def test_calculate_and_print(a_string, b_string, operation_string,expected_string, capsys):
    """
    Tests the calculate_and_print function with various inputs and expected outputs.

    Parameters:
    - a_string (str): The first operand as a string.
    - b_string (str): The second operand as a string.
    - operation_string (str): The operation to perform.
    - expected_string (str): The expected output string.
    - capsys: Pytest fixture for capturing sys.stdout and sys.stderr.

    Asserts that the output of calculate_and_print matches the expected output for each set of parameters.
    """
    calculate_and_print(a_string, b_string, operation_string)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_string
