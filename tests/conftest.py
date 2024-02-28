# conftest.py
"""Module docstring: This module configures pytest options and generates test data for the calculator app."""
# Import pytest for writing test cases.
from decimal import Decimal
import pytest # used to run pytest's pylint: disable=unused-import
from faker import Faker
from calculator.operations import add, subtract, multiply, divide

fake = Faker()

def generate_test_data(num_records):
    """
    Generates test data for a specified number of records. Each record consists of two numbers
    and an arithmetic operation (add, subtract, multiply, divide), along with the expected result
    of applying the operation to those numbers.

    Parameters:
    - num_records (int): The number of test records to generate.

    Yields:
    - tuple: Each containing two Decimal numbers (a, b), an operation name (as a string),
      the operation function (callable), and the expected result (Decimal or string in case of an error).
    """
    # Define operation mappings for both Calculator and Calculation tests
    operation_mappings = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
    }

    # Generate test data
    for _ in range(num_records):
        a = Decimal(fake.random_number(digits=2))
        b = Decimal(fake.random_number(digits=2)) if _ % 4 != 3 else Decimal(fake.random_number(digits=1))
        operation_name = fake.random_element(elements=list(operation_mappings.keys()))
        operation_func = operation_mappings[operation_name]

        # Ensure b is not zero for divide operation to prevent division by zero in expected calculation
        if operation_func == divide: # pylint: disable=comparison-with-callable
            b = Decimal('1') if b == Decimal('0') else b
        try:
            if operation_func == divide and b == Decimal('0'): # pylint: disable=comparison-with-callable
                expected = "ZeroDivisionError"
            else:
                expected = operation_func(a, b)
        except ZeroDivisionError:
            expected = "ZeroDivisionError"

        yield a, b, operation_name, operation_func, expected

def pytest_addoption(parser):
    """
    Generates pytest N number of records when you enter a command of pytest --num_records=N.
    """
    parser.addoption("--num_records", action="store", default=5, type=int, help="Number of test records to generate")

def pytest_generate_tests(metafunc):
    """
    Dynamically generate tests based on the `--num_records` command-line option.
    
    This hook is called by pytest to parameterize tests. It reads the number of records specified 
    by the `--num_records` command-line option and generates test data accordingly, allowing 
    parameterized tests to run with a dynamic set of inputs.
    
    Parameters:
    - metafunc (Metafunc): The metafunc object for the test function to be parameterized.
    """
    # Check if the test is expecting any of the dynamically generated fixtures
    if {"a", "b", "expected"}.intersection(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")
        # Adjust the parameterization to include both operation_name and operation for broad compatibility
        # Ensure 'operation_name' is used for identifying the operation in Calculator class tests
        # 'operation' (function reference) is used for Calculation class tests.
        parameters = list(generate_test_data(num_records))
        # Modify parameters to fit test functions' expectations
        modified_parameters = [(a, b, op_name if 'operation_name' in metafunc.fixturenames else op_func, expected) for a, b, op_name, op_func, expected in parameters]
        metafunc.parametrize("a,b,operation,expected", modified_parameters)
