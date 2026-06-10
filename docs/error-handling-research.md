# Investigación sobre manejo de errores

Notas de investigación que comparan nuestro diseño de excepciones con la
documentación oficial de Python, la guía de buenas prácticas de Real Python
y tres proyectos reales en producción (`requests`, Click y HTTPie). Escrito
para respaldar las decisiones de diseño de `src/services/exceptions.py`.

## Fuentes

- Tutorial de Python — Errores y excepciones: https://docs.python.org/es/3/tutorial/errors.html
- Real Python — Buenas prácticas de manejo de excepciones: https://realpython.com/ref/best-practices/exception-handling/
- requests — `src/requests/exceptions.py`: https://github.com/psf/requests/blob/main/src/requests/exceptions.py
- Click — `src/click/exceptions.py`: https://github.com/pallets/click/blob/main/src/click/exceptions.py
- HTTPie — `httpie/core.py`: https://github.com/httpie/cli/blob/master/httpie/core.py

## Qué dice la documentación oficial

Del tutorial de Python (excepciones definidas por el usuario):

> "Las excepciones, típicamente, deberán derivar de la clase `Exception`,
> directa o indirectamente."

> "Las clases de excepción [...] es habitual mantenerlas lo más simples
> posible, a menudo ofreciendo solo un número de atributos con información
> sobre el error que leerán los gestores de la excepción."

> "La mayoría de las excepciones se definen con nombres acabados en «Error»,
> de manera similar a la nomenclatura de las excepciones estándar."

Conclusión: crear excepciones propias es lo esperado, y deben mantenerse
*simples* — una clase con unos pocos atributos informativos es la norma,
no un signo de sobre-ingeniería.

## Qué recomienda Real Python

- **"Prefiere las excepciones integradas y usa las personalizadas para
  errores de dominio"** — define una *jerarquía pequeña* que herede de
  `Exception` cuando el error pertenece a tu dominio.
- **"Captura la excepción más específica que puedas manejar"** — nunca un
  `except:` desnudo.
- **"Lanza abajo, captura arriba" (raise low, catch high)** — las funciones
  de bajo nivel lanzan; el borde de la aplicación (comando CLI, handler web)
  captura y convierte el error en un mensaje para el usuario. La lógica
  central queda limpia.
- **Usa `raise ... from err`** — conserva el traceback original, que es
  contexto valioso al depurar.

## Qué hacen los proyectos reales en producción

### requests (librería de la que ya dependemos)

Una clase base, `RequestException`, con ~20 subclases — y la mayoría están
**vacías**: un docstring y nada más (`ProxyError`, `SSLError`,
`TooManyRedirects`, `URLRequired`, ...). La subclase *es* la información:
quien llama elige cuánta granularidad capturar (`except Timeout` frente a
`except RequestException`).

Conclusión: las subclases de excepción "vacías" son práctica estándar en una
de las librerías más usadas de Python. No son innecesarias — son la API que
permite a quien llama reaccionar de forma distinta a fallos distintos.

### Click (framework de CLIs)

Una clase base, `ClickException`, que lleva **datos y comportamiento**:

- `message` — el texto que ve el usuario.
- `exit_code` — atributo de clase (1 por defecto, 2 en `UsageError`).
- `format_message()` — devuelve el texto a mostrar; las subclases lo
  sobrescriben (`BadParameter` devuelve `"Invalid value for {param}:
  {message}"`).
- `show()` — imprime el error formateado con el prefijo `Error:`.

Las subclases (`UsageError`, `BadParameter`, `MissingParameter`,
`FileError`...) solo añaden lo que cambia: un atributo, un
`format_message()` sobrescrito, un `exit_code` distinto. Este es el
equivalente pythónico más cercano a "una clase de errores con interfaces y
métodos específicos": en Python no hay interfaces — el idioma es una clase
base con atributos y métodos sobrescribibles.

### HTTPie (app de CLI, la misma forma que nuestro proyecto)

Las funciones internas lanzan libremente; el punto de entrada (`raw_main`)
captura arriba del todo: primero las excepciones específicas
(`requests.Timeout`, `ConnectionError`, `KeyboardInterrupt`...), y un
`Exception` genérico al final como red de seguridad. Cada captura se
convierte en un mensaje claro más un código de salida — el usuario nunca ve
un traceback crudo. Esto es "lanza abajo, captura arriba" aplicado a una CLI
real.

## Decisiones para este proyecto

| Decisión | Tomada de |
| --- | --- |
| Mantener una jerarquía pequeña: una raíz + una base por servicio + hojas específicas | requests, Real Python |
| La raíz `AppError` lleva `default_message`, `hint` opcional y `format_message()` | Click (`ClickException`) |
| Las hojas declaran su propio `default_message`/`hint` — todos los textos de usuario viven en un único archivo (`exceptions.py`), nunca hardcodeados en los `raise` | Click; feedback de la profesora ("mensajes en un archivo") |
| Los servicios lanzan; `App`/`main.py` capturan y muestran vía `ConsoleUI` | HTTPie, Real Python ("lanza abajo, captura arriba") |
| Traducir las excepciones de terceros en el borde con `raise X() from e` (conservando el traceback original) | Real Python |
| Las excepciones nunca imprimen — mostrar es trabajo de la capa de consola | Nuestra arquitectura de tres capas (más estricta que el `show()` de Click) |

Una subclase se gana su sitio cuando cumple al menos uno de estos criterios:

1. Alguien la captura para manejarla de forma distinta (p. ej.
   `ResourceNotFoundError` → volver a pedir el tema en vez de salir;
   `AIAuthError` → capturada en el arranque en `main.py`).
2. Tiene su propio mensaje o hint para el usuario.
3. Un test la usa para documentar un modo de fallo concreto.

Todas las clases de `src/services/exceptions.py` cumplen al menos un
criterio; cualquier clase futura que no cumpla ninguno no debería añadirse.
