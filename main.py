from figuras import (
    Etiqueta,
    Triangulo,
    Cuadrado,
    Pentagono,
    Hexagono,
    Taller,
    exportar_todo,
)
from libreria_externa import PlanoCAD


def main():
    # Creamos los cuatro polígonos.
    triangulo = Triangulo("Triángulo", "rojo", [3, 4, 5])
    cuadrado = Cuadrado("Cuadrado", "azul", [2, 2, 2, 2])
    pentagono = Pentagono.regular("Pentágono", "verde", 2)
    hexagono = Hexagono.regular("Hexágono", "amarillo", 2)

    # Creamos etiquetas inmutables.
    etiqueta_a = Etiqueta("vértice A")
    etiqueta_b = Etiqueta("lado principal")

    # Asociación Lado - Etiqueta.
    triangulo.lados()[0].etiquetar(etiqueta_a)
    cuadrado.lados()[1].etiquetar(etiqueta_b)

    # Creamos un Taller.
    taller = Taller()

    # Agregación:
    # el Taller recibe polígonos que ya existían.
    taller.recibir(triangulo)
    taller.recibir(cuadrado)
    taller.recibir(pentagono)
    taller.recibir(hexagono)

    print("=== INVENTARIO DEL TALLER ===")

    for poligono in taller.inventario():
        print(
            f"{type(poligono).__name__}: "
            f"{poligono.nombre}, "
            f"color={poligono.color}, "
            f"perímetro={poligono.perimetro():.2f}"
        )

    print()

    # Protocol / duck typing:
    # PlanoCAD no hereda de Exportable, pero tiene exportar().
    plano = PlanoCAD("CAD-001", "1:50")

    elementos = [
        triangulo,
        cuadrado,
        pentagono,
        hexagono,
        plano,
    ]

    print("=== EXPORTACIÓN ===")

    for resultado in exportar_todo(elementos):
        print(resultado)

    print()

    # Asociación: mostramos las etiquetas.
    print("=== ETIQUETAS ===")
    print(f"Primer lado del triángulo: {triangulo.lados()[0].etiqueta}")
    print(f"Segundo lado del cuadrado: {cuadrado.lados()[1].etiqueta}")

    print()

    # Copia defensiva del inventario.
    inventario = taller.inventario()
    print(f"Cantidad de polígonos en el taller: {len(inventario)}")

    # Agregación:
    # quitamos el polígono del taller, pero el objeto sigue existiendo.
    taller.restaurar(triangulo)

    print(
        f"Cantidad después de restaurar el triángulo: "
        f"{len(taller.inventario())}"
    )

    print(f"El triángulo sigue existiendo: {triangulo.nombre}")

    print()

    # Falla temprana de la ABC.
    print("=== FALLA TEMPRANA DE LA ABC ===")

    try:
        from figuras import Poligono

        Poligono("Figura abstracta", "gris", [])
    except TypeError as error:
        print(f"Error al construir Poligono abstracto: {error}")


if __name__ == "__main__":
    main()
