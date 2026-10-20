# Sección 2: REST API de Todo.ly

Caso **TC-API-001**: crear un usuario, obtener su token y crear, consultar,
actualizar y eliminar un proyecto con ese token.

Repositorio: https://github.com/nohpedro/API-Testing

## Tecnologías

- Java: JDK 17 o superior compatible con Gradle 9.8.0; validado con OpenJDK 27.
- Gradle Wrapper 9.8.0 (distribución verificada por SHA-256).
- Cucumber Java y JUnit Platform Engine 8.0.4.
- Rest Assured y JSON Schema Validator 6.0.1.
- JUnit Platform 6.0.0 y Jackson Databind 2.22.0.

## Ejecución

Se necesita un **JDK**, acceso a Internet, Maven Central y `https://todo.ly`.
`JAVA_HOME` debe apuntar al JDK; Java 8 no es suficiente.
La primera ejecución descarga Gradle y las dependencias.

```powershell
# Windows / PowerShell, desde la raíz del proyecto
.\gradlew.bat clean test

# Comando compatible con el ejemplo de clase
.\gradlew.bat clean cucumberCli -Psuite="@Seccion2"
```

```bash
# Linux / macOS
./gradlew clean test
```

Para comprobar únicamente la vinculación de los pasos, sin llamar a Todo.ly:

```powershell
.\gradlew.bat clean test -PdryRun=true
```

El modo `dryRun` no valida la API. No debe presentarse su reporte como evidencia
de una prueba de integración. `test` vuelve a ejecutar el escenario en cada
invocación: no reutiliza un resultado anterior como `UP-TO-DATE`.

## Qué valida

1. Creación de un usuario con correo y contraseña aleatorios.
2. Obtención de `TokenString` mediante Basic con esas credenciales.
3. Creación del proyecto con `Token: <TokenString>`.
4. Consulta para comprobar la persistencia de su nombre.
5. Actualización y consulta posterior conservando el mismo `Id`.
6. Eliminación con `Deleted = true` y ausencia en proyectos activos.
7. Eliminación de la cuenta temporal mediante un hook `@After`.

Las respuestas de objetos se comprueban por HTTP 200, contenido JSON, ausencia
de errores de negocio y valores esperados. Las respuestas del proyecto también
se validan con un esquema JSON mínimo (`Id`, `Content`, `Deleted`).

Cada petición de proyecto se construye con una especificación nueva y
autenticación por token. No se reutiliza Basic en esas peticiones. Todo.ly usa
el encabezado `Token`; no se envía `Authorization: Bearer`.

## Diseño clean

```text
src/test/
  java/
    config/Configuration.java       URL y tiempos de espera
    client/ApiClient.java           Transporte HTTP y autenticación
    client/TodoApi.java             Endpoints y cuerpos de dominio
    support/ScenarioContext.java    Datos exclusivos del escenario
    support/ResponseChecks.java     Aserciones reutilizables
    steps/ProjectSteps.java         Pasos Gherkin y hooks
    runner/RunCucumberTest.java     Suite JUnit Platform
  resources/
    features/project_token.feature Caso de prueba ejecutable
    schemas/project.json           Contrato mínimo del proyecto
```

Se adapta el enfoque de `crudProjectClean.feature`, `MyStepdefsClean` y
`client/` del ZIP de clase `api_v6-main.zip`. Se reemplazan las credenciales
fijas por datos temporales y se centraliza el envío HTTP para evitar clases
repetidas por método. No se incorporan los ejemplos ni sus credenciales.

La cuenta pertenece exclusivamente a la ejecución. El hook intenta eliminar
el proyecto si el flujo falla y después elimina la cuenta, incluso si falla
la limpieza del proyecto. Un fallo de limpieza hace fallar el escenario.
Si la API queda inaccesible durante la limpieza, no puede garantizarse la
eliminación remota. No se escriben contraseñas, tokens ni cuerpos sensibles
en logs, reportes o archivos.

## Reportes y entrega

- PDF de entrega: [`output/pdf/seccion2-rest-api-todo-ly.pdf`](output/pdf/seccion2-rest-api-todo-ly.pdf).
- Informe Word editable: [`output/word/seccion2-rest-api-todo-ly.docx`](output/word/seccion2-rest-api-todo-ly.docx).
- Reporte generado por cada ejecución: `build/reports/cucumber/cucumber.html`.
- Resultado estructurado: `build/reports/cucumber/cucumber.json` y `cucumber.xml`.
- Reporte Gradle: `build/reports/tests/test/index.html`.
- Evidencia de la ejecución documentada: [`docs/evidence/`](docs/evidence/).

Las evidencias guardadas son una instantánea; una ejecución nueva genera
reportes en `build/`. Los tiempos son observaciones y no un SLA.

El PDF se puede regenerar con Python y `reportlab`, usando la evidencia guardada:

```powershell
python -m pip install -r tools/requirements.txt
python tools/create_report.py
```

Incidencia durante la preparación: una ejecución anterior dejó una cuenta
temporal sin eliminar porque la ruta de limpieza devolvió 404. La ruta se
corrigió a `/api/user/{id}.json` y la ejecución final eliminó su cuenta
correctamente. Las credenciales de la ejecución anterior no se guardaron,
por lo que esa cuenta no pudo recuperarse para eliminarla. El detalle consta
en `docs/evidence/execution.json`.

## Materiales de referencia

- `api-aut.pdf`, diapositivas de clase, páginas 5-11: HTTP, request/response
  y verificaciones de estado, headers, body, esquema y efectos persistentes.
- `cucum.pdf`, diapositivas de clase, páginas 3-10: BDD, Gherkin, steps, tags y hooks.
- `api_v6-main.zip`, repositorio de ejemplo proporcionado para la actividad.
- [Documentación de Todo.ly](https://todo.ly/ApiWiki/).
- [Compatibilidad de Java y Gradle](https://docs.gradle.org/9.8.0/userguide/compatibility.html).
