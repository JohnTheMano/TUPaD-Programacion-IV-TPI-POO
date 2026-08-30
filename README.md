# TPI Programación IV — Unidad 3

## Descripción

Este proyecto corresponde al Trabajo Práctico Integrador de la Unidad 3 de Programación IV.

El dominio utilizado es el de figuras geométricas, polígonos, lados, etiquetas y un taller.

Se aplican conceptos de Programación Orientada a Objetos en Python, incluyendo:

- Encapsulamiento.
- Herencia.
- Clases abstractas.
- `Protocol`.
- Composición.
- Agregación.
- Asociación.
- Copia defensiva.
- `@dataclass(frozen=True)`.

## Archivos del proyecto

| Archivo | Contenido |
|---|---|
| `figuras.py` | Dominio completo resuelto de las Partes 1 a 4. |
| `parte1_diagnostico.py` | Código de partida de la Parte 1, corregido. |
| `demo_sintomas.py` | Demostración de dos síntomas del código original. |
| `libreria_externa.py` | Clase `PlanoCAD` proporcionada por la consigna. No fue modificada. |
| `main.py` | Demo integradora del proyecto. |
| `informe.md` | Informe correspondiente al trabajo práctico. |
| `uml/modelo_final.md` | Diagrama de clases final en Mermaid. |

## Principales decisiones de diseño

- `Poligono` es una clase abstracta mediante `ABC`.
- `Triangulo`, `Cuadrado`, `Pentagono` y `Hexagono` heredan de `Poligono`.
- `PoligonoRegular` no forma parte de la jerarquía final. Su funcionalidad se reemplaza mediante métodos de clase como `regular()`.
- `Exportable` se implementa mediante `Protocol`.
- `PlanoCAD` cumple el contrato `Exportable` sin modificar la clase de la librería externa.
- `Poligono` compone sus propios objetos `Lado`.
- `Taller` recibe polígonos que ya fueron creados, por lo que la relación es de agregación.
- `Lado` puede tener una `Etiqueta` o ninguna.
- `Etiqueta` se implementa mediante `@dataclass(frozen=True)`.
- `Poligono.lados()` y `Taller.inventario()` utilizan copia defensiva.
- `Lado.longitud` utiliza `@property` porque requiere validación.

## Ejecución

El proyecto requiere Python 3 y utiliza únicamente la biblioteca estándar.

### Demo integradora

Ejecutar:

```bash
python main.py

Este programa muestra:

Los cuatro tipos de polígonos.
El inventario del taller.
Las etiquetas asociadas a lados.
La exportación de polígonos y PlanoCAD.
La relación de agregación entre Taller y Poligono.
Que el polígono continúa existiendo después de retirarlo del taller.
La falla temprana al intentar instanciar Poligono.
Demo de síntomas
Ejecutar:

python demo_sintomas.py

Este programa demuestra dos problemas presentes en el código original:

Argumento por defecto mutable.
Atributo de clase mutable.
También muestra el comportamiento del código después del arreglo.

Diagnóstico corregido
Ejecutar:

python parte1_diagnostico.py

Este archivo contiene la versión corregida del dominio correspondiente a la Parte 1.

Diagrama UML
El diagrama de clases final se encuentra en:

uml/modelo_final.md

Está escrito en formato Mermaid y representa:

Herencia.
Composición.
Agregación.
Asociación.
Cumplimiento del contrato Exportable.
Dependencias
No se utilizan paquetes externos.

El proyecto utiliza únicamente módulos de la biblioteca estándar de Python:

abc
dataclasses
typing
math
Estructura final del proyecto
de_la_Puente_Pablo_TPI_POO/
├── README.md
├── figuras.py
├── parte1_diagnostico.py
├── demo_sintomas.py
├── libreria_externa.py
├── main.py
├── informe.md
└── uml/
    └── modelo_final.md

Preparación de la entrega
Antes de comprimir el proyecto se deben eliminar las carpetas generadas automáticamente, como:

__pycache__/
.venv/

