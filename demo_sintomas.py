class PoligonoOriginal:
    catalogo = []

    def __init__(
        self,
        nombre,
        color,
        lados=[],
        observaciones=[]
    ):
        self._nombre = nombre
        self._color = color
        self._lados = lados
        self._observaciones = observaciones

        PoligonoOriginal.catalogo.append(self)


print("=== SÍNTOMA 1: argumento por defecto mutable ===")

p1 = PoligonoOriginal("P1", "rojo")
p2 = PoligonoOriginal("P2", "azul")

p1._observaciones.append("observación de P1")

print("Observaciones de p1:", p1._observaciones)
print("Observaciones de p2:", p2._observaciones)
print("¿Comparten la misma lista?:", p1._observaciones is p2._observaciones)


print()
print("=== SÍNTOMA 2: atributo de clase mutable ===")

print("Catálogo antes:", PoligonoOriginal.catalogo)

print("Cantidad de elementos:", len(PoligonoOriginal.catalogo))
print(
    "¿p1 y p2 aparecen en el mismo catálogo?:",
    p1 in PoligonoOriginal.catalogo and p2 in PoligonoOriginal.catalogo
)


print()
print("=== DESPUÉS DEL ARREGLO ===")

from figuras import Triangulo, Cuadrado

t = Triangulo("Triángulo", "rojo", [3, 4, 5])
c = Cuadrado.regular("Cuadrado", "azul", 2)

print("Lados de t:", t.lados())
print("Lados de c:", c.lados())
print("Cada polígono crea su propio estado.")