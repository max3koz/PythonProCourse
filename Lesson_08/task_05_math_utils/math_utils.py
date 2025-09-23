def divide(a: int, b: int) -> float:
    """
    Function of the divided two numbers.
    Args:
        a (int): numerator
        b (int): denominator
    Returns:
        float: result of division
    Raises:
        ZeroDivisionError: if b == 0
    """
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    return a / b
