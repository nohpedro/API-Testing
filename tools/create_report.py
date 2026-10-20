"""Genera el PDF de entrega a partir de la evidencia real guardada en docs/evidence."""
import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Preformatted,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/seccion2-rest-api-todo-ly.pdf"
REPO = "https://github.com/nohpedro/API-Testing"
evidence = json.loads((ROOT / "docs/evidence/cucumber.json").read_text(encoding="utf-8"))
scenario = evidence[0]["elements"][0]
steps = scenario["steps"]
hooks = scenario.get("before", []) + scenario.get("after", [])
assert all(s["result"]["status"] == "passed" for s in steps + hooks), "La evidencia debe ser exitosa."
audit = []
for step in steps + hooks:
    audit.extend(step.get("output", []))
requests = [line for line in audit if "| HTTP " in line]
execution = json.loads((ROOT / "docs/evidence/execution.json").read_text(encoding="utf-8"))

navy = colors.HexColor("#132B45")
teal = colors.HexColor("#007C83")
ink = colors.HexColor("#26384A")
muted = colors.HexColor("#576979")
pale = colors.HexColor("#EEF5F7")
line = colors.HexColor("#D9E4E8")
green = colors.HexColor("#087B50")
styles = getSampleStyleSheet()
mono_font = "Courier"
consolas = Path("C:/Windows/Fonts/consola.ttf")
if consolas.exists():
    pdfmetrics.registerFont(TTFont("ConsolasReport", str(consolas)))
    mono_font = "ConsolasReport"
styles.add(ParagraphStyle("Kicker", fontName="Helvetica-Bold", fontSize=9,
                          textColor=teal, spaceAfter=12, tracking=1))
styles.add(ParagraphStyle("TitleReport", fontName="Helvetica-Bold", fontSize=29,
                          leading=34, textColor=navy, spaceAfter=16))
styles.add(ParagraphStyle("Section", fontName="Helvetica-Bold", fontSize=18,
                          leading=22, textColor=navy, spaceAfter=14))
styles.add(ParagraphStyle("Sub", fontName="Helvetica-Bold", fontSize=11,
                          leading=15, textColor=teal, spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle("TextReport", fontName="Helvetica", fontSize=10,
                          leading=15, textColor=ink, spaceAfter=9))
styles.add(ParagraphStyle("SmallReport", fontName="Helvetica", fontSize=8.6,
                          leading=12, textColor=muted, spaceAfter=6))
styles.add(ParagraphStyle("CellReport", fontName="Helvetica", fontSize=8.7,
                          leading=12, textColor=ink))
styles.add(ParagraphStyle("CellHead", fontName="Helvetica-Bold", fontSize=8.6,
                          leading=12, textColor=colors.white))
styles.add(ParagraphStyle("CodeReport", fontName=mono_font, fontSize=8.5 if consolas.exists() else 8,
                          leading=11.5, textColor=ink, backColor=pale,
                          borderPadding=10, spaceAfter=10))

story = []


def para(text, style="TextReport"):
    return Paragraph(text, styles[style])


def p(text, style="TextReport"):
    story.append(para(text, style))


def title(number, text):
    p(f"SECCIÓN 2  /  REST API  /  {number}", "Kicker")
    p(text, "Section")


def table(headers, rows, widths):
    data = [[para(h, "CellHead") for h in headers]]
    data += [[para(str(c), "CellReport") for c in row] for row in rows]
    item = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1)
    item.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), navy),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, pale]),
        ("LINEBELOW", (0, 0), (-1, 0), .7, teal),
        ("LINEBELOW", (0, 1), (-1, -1), .3, line),
    ]))
    story.append(item)
    story.append(Spacer(1, 10))


def code(text):
    story.append(Preformatted(text, styles["CodeReport"]))


def newpage():
    story.append(PageBreak())


title("01", "Automatización de pruebas")
p("Todo.ly<br/>Proyectos con token", "TitleReport")
p("Caso de prueba TC-API-001 · Sección 2 (30%)<br/>20 de octubre de 2026", "SmallReport")
p("Flujo seleccionado", "Sub")
p("Crear un usuario y, con ese usuario, crear, actualizar y eliminar un proyecto "
  "utilizando un token de autenticación. Se añaden consultas para comprobar que "
  "los cambios persisten y que el proyecto eliminado no permanece activo.")
p("Repositorio público del código", "Sub")
p(f'<link href="{REPO}" color="#007C83"><b>{REPO}</b></link>')
p("El repositorio contiene el proyecto Gradle, el escenario Cucumber, las clases Java, "
  "el esquema de validación, la evidencia y este documento.")
table(["Identificación", "Definición"], [
    ["Objetivo", "Comprobar el ciclo de vida de un proyecto perteneciente al usuario "
     "recién creado, con autenticación por token en todas las operaciones del proyecto."],
    ["Tipo y prioridad", "Prueba funcional de integración de extremo a extremo. Prioridad alta."],
    ["Precondiciones", "Todo.ly accesible por HTTPS; JDK compatible; dependencias descargables. "
     "No se requiere una cuenta existente."],
    ["Datos", "Correo único con UUID bajo example.com; contraseña aleatoria; "
     "nombre inicial: Proyecto Seccion 2; nombre actualizado: Proyecto Seccion 2 actualizado."],
    ["Postcondiciones", "Proyecto eliminado y ausente de la lista activa. Cuenta temporal "
     "eliminada mediante el hook de limpieza."],
], [105, 402])
p("Criterio de aprobación", "Sub")
p("El escenario y sus hooks deben finalizar sin errores. Cada operación debe satisfacer "
  "sus aserciones de estado, formato y datos; una respuesta HTTP 200 por sí sola no "
  "demuestra que el flujo sea correcto.")

newpage()
title("02", "Caso de prueba: pasos y resultados")
p("URL base: <b>https://todo.ly</b>. Cuerpos JSON y encabezados "
  "<b>Accept</b> y <b>Content-Type: application/json</b>.")
table(["N°", "Petición / autenticación", "Resultado esperado"], [
    ["1", "<b>POST /api/user.json</b><br/>Sin autenticación.<br/>Email, Password y FullName.",
     "HTTP 200; Id positivo; Email y FullName iguales a los datos enviados."],
    ["2", "<b>GET /api/authentication/token.json</b><br/>Basic con el usuario recién creado.",
     "HTTP 200; TokenString presente y no vacío. Guardar el token en memoria."],
    ["3", "<b>POST /api/projects.json</b><br/>Token; Content inicial.",
     "HTTP 200; Id positivo; Content esperado; Deleted = false. Guardar el Id."],
    ["4", "<b>GET /api/projects/{id}.json</b><br/>Token.",
     "HTTP 200; mismo Id; nombre inicial persistido; Deleted = false."],
    ["5", "<b>PUT /api/projects/{id}.json</b><br/>Token; Content actualizado.",
     "HTTP 200; mismo Id; nuevo Content; Deleted = false."],
    ["6", "<b>GET /api/projects/{id}.json</b><br/>Token.",
     "HTTP 200; mismo Id; nombre actualizado persistido; Deleted = false."],
    ["7", "<b>DELETE /api/projects/{id}.json</b><br/>Token.",
     "HTTP 200; mismo Id; nombre actualizado; Deleted = true."],
    ["8", "<b>GET /api/projects.json</b><br/>Token.",
     "HTTP 200; lista JSON que no contiene el Id del proyecto eliminado."],
    ["9", "<b>DELETE /api/user/{userId}.json</b><br/>Hook @After; Basic de la cuenta temporal.",
     "HTTP 200; Id igual al usuario creado. La limpieza también se comprueba."],
], [34, 224, 249])
p("Validaciones transversales", "Sub")
p("Las respuestas de objetos deben ser JSON y no contener ErrorCode ni ErrorMessage "
  "con valor. Las respuestas de proyecto cumplen un esquema mínimo: Id entero positivo, "
  "Content de texto no vacío y Deleted booleano. Los campos adicionales son válidos.",
  "SmallReport")
p("El resultado esperado de eliminación es HTTP 200 con un objeto marcado como eliminado. "
  "La implementación valida ese contrato concreto de Todo.ly.", "SmallReport")

newpage()
title("03", "Escenario ejecutable y diseño clean")
feature = (ROOT / "src/test/resources/features/project_token.feature").read_text(encoding="utf-8")
code(feature[feature.index("@Seccion2"):])
p("Todo.ly recibe el encabezado <b>Token: &lt;TokenString&gt;</b>. La autenticación "
  "Basic se utiliza para obtener el token y para eliminar la cuenta temporal; "
  "las peticiones de proyecto llevan exclusivamente el token.", "SmallReport")
p("Separación de responsabilidades", "Sub")
table(["Capa", "Responsabilidad"], [
    ["Feature / runner", "Gherkin expresa el comportamiento. RunCucumberTest descubre el escenario con JUnit Platform."],
    ["Steps / contexto", "ProjectSteps coordina acciones y hooks. ScenarioContext conserva los identificadores "
     "y el token sólo durante el escenario."],
    ["Cliente HTTP", "ApiClient centraliza transporte, autenticación y timeout. TodoApi define rutas y cuerpos."],
    ["Validación", "ResponseChecks concentra aserciones comunes; schemas/project.json verifica estructura y tipos."],
], [109, 398])
p("Adaptación del repositorio de clase", "Sub")
p("Se conserva la separación entre escenario, pasos y cliente del ejemplo "
  "crudProjectClean. Se reemplazan las credenciales fijas y la autenticación básica "
  "del CRUD por un usuario temporal y su token. Las peticiones se crean de nuevo "
  "en cada llamada; no hay autenticación global ni estado estático mutable.", "SmallReport")

newpage()
title("04", "Evidencia de ejecución real")
p(f'<font color="#087B50"><b>APROBADO · 1 escenario · {len(steps)} pasos · '
  f'{len(hooks)} hooks sin fallos</b></font>')
p(f"Ejecución: {escape(execution['executed_at_local'])} (America/La_Paz).<br/>"
  "Entorno: Windows, OpenJDK 27 y Gradle Wrapper 9.8.0.<br/>"
  "Comando: <b>.\\gradlew.bat clean test --no-daemon</b>.", "SmallReport")
rows = []
for entry in requests:
    parts = entry.split(" | ")
    rows.append([parts[0], parts[1].replace("auth=", ""),
                 parts[2].replace("HTTP ", ""), parts[3]])
table(["Operación registrada", "Autenticación", "HTTP", "Tiempo"], rows, [270, 109, 48, 80])
p("Qué demuestra esta ejecución", "Sub")
p("Los pasos y las validaciones se ejecutaron contra el servicio real. Las llamadas "
  "del proyecto registraron autenticación Token; las verificaciones de contenido, "
  "identidad, esquema, persistencia y ausencia de la lista activa pasaron. "
  "El hook completó la eliminación de la cuenta temporal.")
p("Evidencia reproducible", "Sub")
p(f'Los resultados estructurados están en '
  f'<link href="{REPO}/tree/main/docs/evidence" color="#007C83">docs/evidence/</link>: '
  "cucumber.json, cucumber.xml, cucumber.html y execution.json. "
  "El JSON conserva el estado de cada paso y hook, además de los registros HTTP "
  "mostrados en esta página.", "SmallReport")
p("Los tiempos son mediciones de esta ejecución y no un umbral de rendimiento. "
  "Esta evidencia cubre el flujo positivo seleccionado; no demuestra cobertura "
  "de casos negativos, carga o seguridad integral.", "SmallReport")
p("Incidencia durante la preparación: una ejecución previa dejó una cuenta temporal "
  "porque la ruta de limpieza respondió 404. Se corrigió para incluir el Id. "
  "La cuenta anterior no pudo recuperarse porque sus credenciales no se guardaron; "
  "la ejecución final aquí documentada sí eliminó su cuenta.", "SmallReport")

newpage()
title("05", "Reproducción y referencias")
p("Preparar y ejecutar", "Sub")
p("Instalar un JDK compatible con Gradle 9.8.0 y configurar JAVA_HOME. Se validó "
  "con OpenJDK 27; Java 8 no sirve para estas dependencias. La primera ejecución "
  "necesita Internet para descargar Gradle y las bibliotecas.")
code("git clone https://github.com/nohpedro/API-Testing.git\n"
     "cd API-Testing\n"
     ".\\gradlew.bat clean test\n\n"
     "# Alternativa por etiqueta, como en el ejemplo de clase:\n"
     '.\\gradlew.bat clean cucumberCli -Psuite="@Seccion2"\n\n'
     "# Linux / macOS:\n"
     "./gradlew clean test")
p("Abrir build/reports/cucumber/cucumber.html para consultar los pasos y "
  "build/reports/tests/test/index.html para el resultado de Gradle. "
  "La tarea clean borra los resultados generados de la ejecución anterior.", "SmallReport")
p("Versiones fijadas", "Sub")
p("Gradle 9.8.0; Cucumber 8.0.4; Rest Assured y JSON Schema Validator 6.0.1; "
  "JUnit Platform 6.0.0; Jackson Databind y módulo JDK8 2.22.0. "
  "El código se compila con nivel de lenguaje Java 17.")
p("Limpieza y protección de datos", "Sub")
p("La contraseña y el token se generan u obtienen en ejecución y permanecen en memoria. "
  "Los reportes incluyen método, ruta, modalidad de autenticación, estado y tiempo; "
  "no imprimen credenciales ni cuerpos sensibles. Si falla el flujo, @After intenta "
  "eliminar el proyecto pendiente y después la cuenta. Una caída del servicio durante "
  "la limpieza puede impedir la eliminación remota.")
p("Relación con los materiales proporcionados", "Sub")
p("<b>api-aut.pdf, páginas 5-11:</b> se aplican los métodos HTTP, encabezados y cuerpos JSON; "
  "se verifican código, contenido, esquema y efectos persistentes.<br/>"
  "<b>cucum.pdf, páginas 3-10:</b> se aplican BDD, Gherkin, definiciones de pasos, "
  "etiquetas y hooks.<br/>"
  "<b>api_v6-main.zip:</b> se toma como referencia build.gradle, el paquete client, "
  "MyStepdefsClean y crudProjectClean.feature.", "SmallReport")
p("Referencias consultadas", "Sub")
p('<link href="https://todo.ly/ApiWiki/" color="#007C83">Todo.ly API Wiki</link>'
  " - recursos User, Projects y Authentication.<br/>"
  '<link href="https://docs.gradle.org/9.8.0/userguide/compatibility.html" color="#007C83">'
  "Gradle 9.8.0: matriz de compatibilidad de Java</link>.<br/>"
  "Materiales de clase facilitados para esta actividad. Consulta: 20/10/2026.",
  "SmallReport")


def decoration(canvas, doc):
    w, h = A4
    canvas.setFillColor(teal)
    canvas.rect(0, h-9, w, 9, fill=1, stroke=0)
    canvas.setStrokeColor(line)
    canvas.line(44, 43, w-44, 43)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(muted)
    canvas.drawString(44, 29, "API TESTING  /  TODO.LY  /  TC-API-001")
    canvas.drawRightString(w-44, 29, f"{doc.page} / 5")


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=44, leftMargin=44,
                        topMargin=38, bottomMargin=58, title="Sección 2 - REST API Todo.ly",
                        author="nohpedro", subject="Caso de prueba con Java, Gradle, Cucumber y Rest Assured")
doc.build(story, onFirstPage=decoration, onLaterPages=decoration)
print(OUTPUT)
