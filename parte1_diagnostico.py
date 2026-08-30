import math
from abc import ABC, abstractmethod


class Figura(ABC):
    def __init__(self, nombre: str, color: str) -> None:
        self._nombre = nombre
        self._color = color

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def color(self) -> str:
        return self._color

    @abstractmethod
    def area(self) -> float:
        ...


class Lado:
    def __init__(self, longitud: float) -> None:
        self._longitud = self._validar(longitud)

    @staticmethod
    def _validar(valor: float) -> float:
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        return float(valor)

    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        self._longitud = self._validar(valor)


class Poligono(Figura):
    def __init__(
        self,
        nombre: str,
        color: str,
        longitudes: list[float]
    ) -> None:
        super().__init__(nombre, color)

        esperados = self.lados_esperados()

        if len(longitudes) != esperados:
            raise ValueError(
                f"{type(self).__name__} espera {esperados} lados, "
                f"recibió {len(longitudes)}"
            )

        self._lados = [Lado(longitud) for longitud in longitudes]
        self._observaciones: list[str] = []

    @abstractmethod
    def lados_esperados(self) -> int:
        ...

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def area(self) -> float:
        n = self.lados_esperados()
        lado = self._lados[0].longitud

        return (n * lado ** 2) / (
            4 * math.tan(math.pi / n)
        )

    def lados(self) -> tuple[Lado, ...]:
        return tuple(self._lados)

    def observar(self, texto: str) -> None:
        self._observaciones.append(texto)


class Triangulo(Poligono):
    def lados_esperados(self) -> int:
        return 3

    @classmethod
    def equilatero(
        cls,
        nombre: str,
        color: str,
        longitud: float
    ) -> "Triangulo":
        return cls(nombre, color, [longitud] * 3)


class Cuadrado(Poligono):
    def lados_esperados(self) -> int:
        return 4

    @classmethod
    def regular(
        cls,
        nombre: str,
        color: str,
        longitud: float
    ) -> "Cuadrado":
        return cls(nombre, color, [longitud] * 4)


if __name__ == "__main__":
    triangulo = Triangulo("Triángulo", "rojo", [3, 4, 5])
    cuadrado = Cuadrado.regular("Cuadrado", "azul", 2)

    print(f"Perímetro del triángulo: {triangulo.perimetro():g}")
    print(f"Perímetro del cuadrado: {cuadrado.perimetro():g}")
    print(f"Área del cuadrado: {cuadrado.area():.2f}")
    print(f"Nombre: {triangulo.nombre}")