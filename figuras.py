import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from libreria_externa import PlanoCAD


class Exportable(Protocol):
    def exportar(self) -> str:
        ...


@dataclass(frozen=True)
class Etiqueta:
    texto: str


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
    def __init__(
        self,
        longitud: float,
        etiqueta: Etiqueta | None = None
    ) -> None:
        self._longitud = self._validar(longitud)

        # Asociación 0..1:
        # un Lado puede tener una Etiqueta o ninguna.
        self._etiqueta = etiqueta

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

    @property
    def etiqueta(self) -> Etiqueta | None:
        return self._etiqueta

    def etiquetar(self, etiqueta: Etiqueta) -> None:
        self._etiqueta = etiqueta

    def escalar(self, factor: float) -> None:
        if factor <= 0:
            raise ValueError("El factor debe ser positivo")

        self._longitud *= factor


class Poligono(Figura, ABC):
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

        # Composición:
        # el Polígono crea sus propios Lado.
        self._lados = [Lado(longitud) for longitud in longitudes]

    @abstractmethod
    def lados_esperados(self) -> int:
        ...

    def area(self) -> float:
        n = self.lados_esperados()
        lado = self._lados[0].longitud

        return (n * lado ** 2) / (
            4 * math.tan(math.pi / n)
        )

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def lados(self) -> tuple[Lado, ...]:
        # Copia defensiva.
        return tuple(self._lados)

    def exportar(self) -> str:
        return (
            f"{type(self).__name__}: "
            f"{self.nombre}, color={self.color}, "
            f"lados={self.lados_esperados()}"
        )


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


class Pentagono(Poligono):
    def lados_esperados(self) -> int:
        return 5

    @classmethod
    def regular(
        cls,
        nombre: str,
        color: str,
        longitud: float
    ) -> "Pentagono":
        return cls(nombre, color, [longitud] * 5)


class Hexagono(Poligono):
    def lados_esperados(self) -> int:
        return 6

    @classmethod
    def regular(
        cls,
        nombre: str,
        color: str,
        longitud: float
    ) -> "Hexagono":
        return cls(nombre, color, [longitud] * 6)


class Taller:
    def __init__(self) -> None:
        # Agregación:
        # el Taller recibe Poligonos ya existentes.
        self._poligonos: list[Poligono] = []

    def recibir(self, poligono: Poligono) -> None:
        self._poligonos.append(poligono)

    def restaurar(self, poligono: Poligono) -> None:
        if poligono in self._poligonos:
            self._poligonos.remove(poligono)

    def inventario(self) -> tuple[Poligono, ...]:
        # Copia defensiva.
        return tuple(self._poligonos)


def exportar_todo(items: list[Exportable]) -> list[str]:
    return [item.exportar() for item in items]
