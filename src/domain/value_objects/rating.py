class Rating:

    APPROVAL_THRESHOLD = 70

    def __init__(self, value: int):
        if not 0 <= value <= 100:
            raise ValueError(f"Rating must be between 0 and 100, got {value}")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def in_range(self) -> bool:
        """Determina si la calificacion supera el umbral de aprobacion (70)."""
        return self._value > self.APPROVAL_THRESHOLD

# APPROVAL_THRESHOLD va dentro de la clase porque es una regla de negocio
# propia de Rating. Iria fuera solo si multiples clases la necesitaran.

# ValueError es una excepcion built-in de Python.
# Otras comunes: TypeError, KeyError, IndexError, AttributeError.

# raise es el throw de Java. La unica diferencia es que raise solo (sin
# argumento) re-lanza la excepcion activa.

# _value con guion bajo es la convencion de "atributo privado" en Python.
# Ademas, si usaras self.value chocaria con el @property y causaria
# recursion infinita.

# @property permite acceder a _value como rating.value en lugar de
# rating.getValue(). Se lee como atributo pero ejecuta el metodo,
# y sin un setter no se puede modificar desde afuera.

