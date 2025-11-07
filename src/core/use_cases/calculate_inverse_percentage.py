from typing import Union

def calculate_inverse_percentage(total_value: Union[float, int], partial_value: Union[float, int]) -> float:
    """
    Calcula qué porcentaje representa un valor parcial de un valor total.

    Esta función representa una regla de negocio principal y pura. Recibe un valor total
    y un valor parcial, y devuelve el porcentaje correspondiente.

    Args:
        total_value (Union[float, int]): El valor total o base (100%).
        partial_value (Union[float, int]): El valor parcial del que se quiere saber el porcentaje.

    Returns:
        float: El porcentaje que el valor parcial representa del valor total.
    
    Raises:
        ValueError: Si las entradas no son valores numéricos.
        ZeroDivisionError: Si el valor total es cero.
    """
    if not isinstance(total_value, (int, float)) or not isinstance(partial_value, (int, float)):
        raise ValueError("Las entradas deben ser valores numéricos.")

    if total_value == 0:
        raise ZeroDivisionError("El valor total no puede ser cero.")

    return (partial_value / total_value) * 100
