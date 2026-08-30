# Informe — TPI Programación IV, Unidad 3

## Parte 1 — Los 8 java-ismos

| # | Java-ismo | Dónde (clase.método) | Inversión que lo explica | Síntoma observable |
|---|---|---|---|---|
| 1 | Getters preventivos sin lógica | `Figura.getNombre()` / `Figura.getColor()` | Encapsulamiento por convención: en Python se accede al atributo directamente; `@property` se reserva para lógica real. | El cliente debe escribir `getNombre()` para obtener un dato sin transformación ni validación. |
| 2 | Argumentos por defecto mutables | `Poligono.__init__()` | Declaración → runtime: los valores por defecto se crean una sola vez y son compartidos entre llamadas. Se usa `None` y se crea el estado dentro del constructor. | Dos polígonos creados sin observaciones pueden compartir la misma lista de observaciones. |
| 3 | Atributo de clase mutable | `Poligono.catalogo` | El estado que pertenece a cada objeto debe vivir en la instancia, no en un atributo de clase mutable compartido accidentalmente. | Todas las instancias modifican el mismo `catalogo`. |
| 4 | Olvido de `super().__init__()` | `Poligono.__init__()` | Herencia → reutilización real: si la subclase es una `Figura`, debe ejecutar la inicialización común del padre en lugar de copiarla manualmente. | Se duplican `_nombre` y `_color` y no se ejecuta la inicialización de `Figura`. |
| 5 | Type hint incorrecto / contrato falso | `Poligono.area()` | Los type hints describen el contrato del código; no son decoración. La declaración debe coincidir con el comportamiento real. | El método declara `int` pero devuelve un `str`. |
| 6 | Sobrecarga de constructor estilo Java | `Triangulo.__init__()` / `Cuadrado.__init__()` | Declaración → runtime: Python no necesita varios constructores diferenciados por firmas; los constructores alternativos pueden expresarse mediante `@classmethod`. | Un único `__init__` necesita `*args`, `len()` y `isinstance()` para decidir qué construcción realizar. |
| 7 | Acumulador manual | `Poligono.perimetro()` | Traducción con criterio: una operación de recorrido y acumulación se expresa directamente con `sum()` y una expresión generadora. | Hay varias líneas para realizar una suma que puede expresarse en una sola operación. |
| 8 | Falta de copia defensiva | `Poligono.__init__()` / `Poligono.lados()` | Encapsulamiento por convención: proteger el estado interno incluye evitar que una referencia externa modifique directamente el contenedor interno. | El llamador puede modificar la lista original o la lista devuelta y alterar el estado del polígono. |

## Síntomas reproducibles

En `demo_sintomas.py` se reproducen dos problemas del código original: el argumento por defecto mutable hace que distintas instancias compartan la misma lista de observaciones, y el atributo de clase `catalogo` hace que todas las instancias compartan ese estado.

Para la copia defensiva, el código corregido devuelve una copia mediante `tuple(self._lados)`, evitando entregar directamente el contenedor interno.

## Getter convertido en `@property`

El getter de `Lado` sí tenía una razón para convertirse en `@property`: el atributo `longitud` tiene lógica de validación mediante el setter. El acceso del cliente cambia de `lado.getLongitud()` a `lado.longitud`, pero la idea es que el atributo se comporte como un atributo normal y la validación quede encapsulada.

Los getters de `Figura`, en cambio, no necesitan métodos `getNombre()` ni `getColor()`: se accede mediante `figura.nombre` y `figura.color`.

## Parte 2 — Relaciones estructurales

Las tres relaciones usan una asignación de referencia similar, pero se diferencian por el ciclo de vida.

- **Composición `Poligono — Lado`:** en `Poligono.__init__()` se crean los `Lado` dentro del propio polígono: `self._lados = [Lado(longitud) for longitud in longitudes]`. El polígono controla la creación y los lados forman parte de su estructura.
- **Agregación `Taller — Poligono`:** en `Taller.recibir()` se guarda un polígono que ya fue creado afuera: `self._poligonos.append(poligono)`. El taller no lo fabrica ni controla su existencia; solamente lo recibe.
- **Asociación `Lado — Etiqueta`:** `Lado` recibe una `Etiqueta` opcional en su constructor mediante `self._etiqueta = etiqueta`. La etiqueta puede existir independientemente del lado.

En las relaciones con multiplicidad `*`, se aplica copia defensiva: `Poligono.lados()` y `Taller.inventario()` devuelven una tupla para no exponer la lista interna.

## Parte 3 — PoligonoRegular

`Poligono` permanece como superclase porque el dominio afirma que un triángulo, cuadrado, pentágono y hexágono **son polígonos**, y además comparten implementación. Por eso la herencia no existe solamente para conseguir un tipo común.

`PoligonoRegular`, en cambio, no se mantiene como una subclase artificial de `Poligono`. Su función de representar una forma regular se resuelve mediante constructores alternativos como `Cuadrado.regular()`, `Pentagono.regular()` y `Hexagono.regular()`. De esta manera se elimina una jerarquía que no aporta una relación de dominio necesaria.

Además, `Poligono` es una `ABC` y `lados_esperados()` es abstracto. Por eso intentar construir directamente un `Poligono` falla al construir, antes de utilizarlo.

## Parte 4 — ABC vs. Protocol

`Exportable` se modela mediante `Protocol` porque el contrato debe poder ser cumplido por clases que no conocen nuestra jerarquía.

`Poligono` tiene `exportar()` y `PlanoCAD` también tiene `exportar()`, pero `PlanoCAD` pertenece a una librería externa y no puede modificarse para heredar de nuestro contrato. Con `Protocol`, alcanza con que tenga el método requerido: el cumplimiento es estructural.

Por eso la elección no la decide el lenguaje de manera automática: **la decide el diseño del problema**. `ABC` es adecuada para `Poligono` porque existe una jerarquía de dominio y código común. `Protocol` es adecuado para `Exportable` porque queremos un contrato que también puedan cumplir clases externas sin acoplarlas a nuestra jerarquía.

## Tabla de equivalencias

| Elemento en Java | Cómo quedó en mi código Python | ¿Traducción directa o rediseño? | Por qué |
|---|---|---|---|
| Getter `getNombre()` | `nombre` mediante `@property` | Rediseño | En Python el acceso a datos simples no necesita getter preventivo. |
| Setter con validación | `longitud` mediante `@property` y setter | Rediseño | La validación justifica la property porque protege una invariante. |
| Constructor sobrecargado | `@classmethod regular()` / `equilatero()` | Rediseño | Python no necesita simular sobrecarga con `*args` e `isinstance()`. |
| Clase abstracta `Poligono` | `ABC` + `@abstractmethod` | Traducción con adaptación | La relación de dominio se mantiene y Python proporciona el mecanismo abstracto correspondiente. |
| Interfaz `Exportable` | `Protocol` | Rediseño | `PlanoCAD` no puede modificar su herencia, por lo que se necesita un contrato estructural. |
| `equals` / datos de objetos | `@dataclass(frozen=True)` en `Etiqueta` | Rediseño | Python proporciona una forma directa de declarar objetos de datos inmutables. |
| Lista expuesta | `tuple(self._lados)` / `tuple(self._poligonos)` | Rediseño | La copia defensiva evita que el cliente modifique el contenedor interno. |

## Cierre

Al pasar de Java a Python no cambió el modelo principal del dominio: siguen existiendo Figura, Poligono, sus subclases, Lado, Taller y Etiqueta, y se mantienen las relaciones de composición, agregación y asociación. Lo que cambió fue la forma de expresar algunas decisiones: desaparecen getters preventivos, la sobrecarga simulada de constructores y la necesidad de herencia únicamente para conseguir un tipo común. Python permite expresar esos casos mediante atributos, `@property`, `@classmethod`, comprehensions, `ABC` y `Protocol`. La herencia que sí representa un `es-un` del dominio se mantiene.


<!-- # Informe — TPI Programación IV, Unidad 3

## Parte 1 — Los 8 java-ismos

| # | Java-ismo | Dónde (clase.método) | Inversión que lo explica | Síntoma observable |
|---|---|---|---|---|
| 1 | Getters preventivos sin lógica | `Figura.getNombre()` / `Figura.getColor()` | Encapsulamiento por convención: en Python se accede al atributo directamente; `@property` se reserva para lógica real. | El cliente debe escribir `getNombre()` para obtener un dato sin transformación ni validación. |
| 2 | Argumentos por defecto mutables | `Poligono.__init__()` | Declaración → runtime: los valores por defecto se crean una sola vez y son compartidos entre llamadas. Se usa `None` y se crea el estado dentro del constructor. | Dos polígonos creados sin observaciones pueden compartir la misma lista de observaciones. |
| 3 | Atributo de clase mutable | `Poligono.catalogo` | El estado que pertenece a cada objeto debe vivir en la instancia, no en un atributo de clase mutable compartido accidentalmente. | Todas las instancias modifican el mismo `catalogo`. |
| 4 | Olvido de `super().__init__()` | `Poligono.__init__()` | Herencia → reutilización real: si la subclase es una `Figura`, debe ejecutar la inicialización común del padre en lugar de copiarla manualmente. | Se duplican `_nombre` y `_color` y no se ejecuta la inicialización de `Figura`. |
| 5 | Type hint incorrecto / contrato falso | `Poligono.area()` | Los type hints describen el contrato del código; no son decoración. La declaración debe coincidir con el comportamiento real. | El método declara `int` pero devuelve un `str`. |
| 6 | Sobrecarga de constructor estilo Java | `Triangulo.__init__()` / `Cuadrado.__init__()` | Declaración → runtime: Python no necesita varios constructores diferenciados por firmas; los constructores alternativos pueden expresarse mediante `@classmethod`. | Un único `__init__` necesita `*args`, `len()` y `isinstance()` para decidir qué construcción realizar. |
| 7 | Acumulador manual | `Poligono.perimetro()` | Traducción con criterio: una operación de recorrido y acumulación se expresa directamente con `sum()` y una expresión generadora. | Hay varias líneas para realizar una suma que puede expresarse en una sola operación. |
| 8 | Falta de copia defensiva | `Poligono.__init__()` / `Poligono.lados()` | Encapsulamiento por convención: proteger el estado interno incluye evitar que una referencia externa modifique directamente el contenedor interno. | El llamador puede modificar la lista original o la lista devuelta y alterar el estado del polígono. |

## Síntomas reproducibles

En `demo_sintomas.py` se reproducen dos problemas del código original: el argumento por defecto mutable hace que distintas instancias compartan la misma lista de observaciones, y el atributo de clase `catalogo` hace que todas las instancias compartan ese estado.

Para la copia defensiva, el código corregido devuelve una copia mediante `tuple(self._lados)`, evitando entregar directamente el contenedor interno.

## Getter convertido en `@property`

El getter de `Lado` sí tenía una razón para convertirse en `@property`: el atributo `longitud` tiene lógica de validación mediante el setter. El acceso del cliente cambia de `lado.getLongitud()` a `lado.longitud`, pero la idea es que el atributo se comporte como un atributo normal y la validación quede encapsulada.

Los getters de `Figura`, en cambio, no necesitan métodos `getNombre()` ni `getColor()`: se accede mediante `figura.nombre` y `figura.color`.

## Parte 2 — Relaciones estructurales

Las tres relaciones usan una asignación de referencia similar, pero se diferencian por el ciclo de vida.

- **Composición `Poligono — Lado`:** en `Poligono.__init__()` se crean los `Lado` dentro del propio polígono: `self._lados = [Lado(longitud) for longitud in longitudes]`. El polígono controla la creación y los lados forman parte de su estructura.
- **Agregación `Taller — Poligono`:** en `Taller.recibir()` se guarda un polígono que ya fue creado afuera: `self._poligonos.append(poligono)`. El taller no lo fabrica ni controla su existencia; solamente lo recibe.
- **Asociación `Lado — Etiqueta`:** `Lado` recibe una `Etiqueta` opcional en su constructor mediante `self._etiqueta = etiqueta`. La etiqueta puede existir independientemente del lado.

En las relaciones con multiplicidad `*`, se aplica copia defensiva: `Poligono.lados()` y `Taller.inventario()` devuelven una tupla para no exponer la lista interna.

## Parte 3 — PoligonoRegular

`Poligono` permanece como superclase porque el dominio afirma que un triángulo, cuadrado, pentágono y hexágono **son polígonos**, y además comparten implementación. Por eso la herencia no existe solamente para conseguir un tipo común.

`PoligonoRegular`, en cambio, no se mantiene como una subclase artificial de `Poligono`. Su función de representar una forma regular se resuelve mediante constructores alternativos como `Cuadrado.regular()`, `Pentagono.regular()` y `Hexagono.regular()`. De esta manera se elimina una jerarquía que no aporta una relación de dominio necesaria.

Además, `Poligono` es una `ABC` y `lados_esperados()` es abstracto. Por eso intentar construir directamente un `Poligono` falla al construir, antes de utilizarlo.

## Parte 4 — ABC vs. Protocol

`Exportable` se modela mediante `Protocol` porque el contrato debe poder ser cumplido por clases que no conocen nuestra jerarquía.

`Poligono` tiene `exportar()` y `PlanoCAD` también tiene `exportar()`, pero `PlanoCAD` pertenece a una librería externa y no puede modificarse para heredar de nuestro contrato. Con `Protocol`, alcanza con que tenga el método requerido: el cumplimiento es estructural.

Por eso la elección no la decide el lenguaje de manera automática: **la decide el diseño del problema**. `ABC` es adecuada para `Poligono` porque existe una jerarquía de dominio y código común. `Protocol` es adecuado para `Exportable` porque queremos un contrato que también puedan cumplir clases externas sin acoplarlas a nuestra jerarquía.

## Tabla de equivalencias

| Elemento en Java | Cómo quedó en mi código Python | ¿Traducción directa o rediseño? | Por qué |
|---|---|---|---|
| Getter `getNombre()` | `nombre` mediante `@property` | Rediseño | En Python el acceso a datos simples no necesita getter preventivo. |
| Setter con validación | `longitud` mediante `@property` y setter | Rediseño | La validación justifica la property porque protege una invariante. |
| Constructor sobrecargado | `@classmethod regular()` / `equilatero()` | Rediseño | Python no necesita simular sobrecarga con `*args` e `isinstance()`. |
| Clase abstracta `Poligono` | `ABC` + `@abstractmethod` | Traducción con adaptación | La relación de dominio se mantiene y Python proporciona el mecanismo abstracto correspondiente. |
| Interfaz `Exportable` | `Protocol` | Rediseño | `PlanoCAD` no puede modificar su herencia, por lo que se necesita un contrato estructural. |
| `equals` / datos de objetos | `@dataclass(frozen=True)` en `Etiqueta` | Rediseño | Python proporciona una forma directa de declarar objetos de datos inmutables. |
| Lista expuesta | `tuple(self._lados)` / `tuple(self._poligonos)` | Rediseño | La copia defensiva evita que el cliente modifique el contenedor interno. |

## Cierre

Al pasar de Java a Python no cambió el modelo principal del dominio: siguen existiendo Figura, Poligono, sus subclases, Lado, Taller y Etiqueta, y se mantienen las relaciones de composición, agregación y asociación. Lo que cambió fue la forma de expresar algunas decisiones: desaparecen getters preventivos, la sobrecarga simulada de constructores y la necesidad de herencia únicamente para conseguir un tipo común. Python permite expresar esos casos mediante atributos, `@property`, `@classmethod`, comprehensions, `ABC` y `Protocol`. La herencia que sí representa un `es-un` del dominio se mantiene. -->