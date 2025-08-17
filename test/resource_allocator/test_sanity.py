import pytest
from src.resource_allocator.allocate import allocate, Customer

def _are_lists_identical(list_a: list[float], list_b: list[float]) -> bool:
    if len(list_a) != len(list_b):
        return False

    for i in range(len(list_a)):
        if abs(list_a[i] - list_b[i]) > 0.0001:
            return False

    return True

def test_1():
    customers = [
        Customer(10, 1, 1),
        Customer(10, 1, 1)
    ]
    result = allocate(20, customers)
    expected = [10, 10]
    assert _are_lists_identical(result, expected)

def test_2():
    customers = [
        Customer(10, 1, 1),
        Customer(10, 1, 1)
    ]
    result = allocate(23, customers)
    expected = [11.5, 11.5]
    assert _are_lists_identical(result, expected)

def test_3():
    customers = [
        Customer(10, 4, 1),
        Customer(10, 1, 1)
    ]
    result = allocate(30, customers)
    expected = [18, 12]
    assert _are_lists_identical(result, expected)

def test_4():
    customers = [
        Customer(10, 2, 3),
        Customer(10, 1, 2)
    ]
    result = allocate(10, customers)
    expected = [4, 6]
    assert _are_lists_identical(result, expected)

def test_5():
    customers = [
        Customer(20, 1, 1),
        Customer(5, 1, 1),
        Customer(15, 1, 1)
    ]
    result = allocate(10, customers)
    expected = [7.5, 0, 2.5]
    assert _are_lists_identical(result, expected)

def test_6():
    customers = [
        Customer(19, 1, 1),
        Customer(5, 1, 1),
        Customer(11, 1, 1),
        Customer(15, 1, 1)
    ]
    result = allocate(10, customers)
    expected = [7, 0, 0, 3]
    assert _are_lists_identical(result, expected)


@pytest.mark.parametrize("amount,customers,expected", [
    (10, [Customer(19, 1, 1), Customer(5, 1, 1), Customer(11, 1, 1), Customer(15, 1, 1)], [7, 0, 0, 3]),
    (80, [Customer(10, 1, 1), Customer(10, 1, 1), Customer(10, 1, 1), Customer(10, 1, 1)], [20, 20, 20, 20]),
    (80, [Customer(1, 1, 1), Customer(1, 1, 1), Customer(1, 1, 1), Customer(1, 1, 1)], [20, 20, 20, 20]),
    (100, [Customer(10, 2, 1), Customer(10, 1, 1), Customer(10, 1, 1), Customer(10, 1, 1)], [34, 22, 22, 22]),
    (4, [Customer(10, 1, 1), Customer(10, 1, 1), Customer(10, 1, 1), Customer(10, 1, 1)], [1, 1, 1, 1]),
    (0, [Customer(10, 1, 1), Customer(10, 1, 1), Customer(10, 1, 1), Customer(10, 1, 1)], [0, 0, 0, 0])
])
def test_7(amount, customers, expected):
    assert _are_lists_identical(allocate(amount, customers), expected)