classDiagram

class Exportable {
    <<Protocol>>
    +exportar() str
}

class Figura {
    <<abstract>>
    #_nombre str
    #_color str
    +nombre str
    +color str
    +area() float
}

class Poligono {
    <<abstract>>
    #_lados list~Lado~
    +lados_esperados() int
    +perimetro() float
    +lados() tuple~Lado~
    +exportar() str
}

class Lado {
    #_longitud float
    #_etiqueta Etiqueta
    +longitud float
    +etiqueta Etiqueta
    +escalar(factor) None
    +etiquetar(etiqueta) None
}

class Etiqueta {
    <<frozen dataclass>>
    +texto str
}

class Taller {
    #_poligonos list~Poligono~
    +recibir(poligono) None
    +restaurar(poligono) None
    +inventario() tuple~Poligono~
}

class Triangulo {
    +lados_esperados() int
    +equilatero(nombre, color, longitud) Triangulo
}

class Cuadrado {
    +lados_esperados() int
    +regular(nombre, color, longitud) Cuadrado
}

class Pentagono {
    +lados_esperados() int
    +regular(nombre, color, longitud) Pentagono
}

class Hexagono {
    +lados_esperados() int
    +regular(nombre, color, longitud) Hexagono
}

class PlanoCAD {
    <<librería externa>>
    +exportar() str
}

Figura <|-- Poligono

Poligono <|-- Triangulo
Poligono <|-- Cuadrado
Poligono <|-- Pentagono
Poligono <|-- Hexagono

Poligono "1" *-- "3..*" Lado : composición
Lado "1" --> "0..1" Etiqueta : asociación
Taller "1" o-- "0..*" Poligono : agregación

Poligono ..|> Exportable : cumple
PlanoCAD ..|> Exportable : cumple estructuralmente
