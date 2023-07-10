"""
CLI Solicitudes

Una solicitud es una petición de un cliente para descargar un archivo.

Son creadas por plataforma-web-api-new directamente en Redis.

Se validan los campos y si cumple con los requisitos se converten en Mensajes.

"""
from datetime import datetime
import json
import re

import rich
import typer

from config.settings import GCS_BUCKETS
from lib.redis import redis_client
from lib.safe_string import EMAIL_REGEXP, URL_PDF_FILE_REGEXP

QUEUE = "hermes_solicitudes"

app = typer.Typer()


@app.command()
def consultar():
    """
    Consultar solicitudes
    """
    rich.print("Consultar solicitudes")

    # Obtener la cantidad de solicitudes
    count = redis_client.llen(QUEUE)

    # Si no hay solicitudes
    if not count:
        rich.print("[red]No hay solicitudes[/red]")
        raise typer.Exit(code=0)

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for encabezado in ["Correo electrónico", "Depósito", "Tiempo", "Token", "URL"]:
        table.add_column(encabezado)
    for _ in range(count):
        # Obtener el primer elemento de la cola
        solicitud_str = redis_client.lindex(QUEUE, _)

        # Cargar datos de la solicitud
        solicitud = json.loads(solicitud_str)

        # Agregar una fila a la tabla
        table.add_row(
            solicitud["correo_electronico"],
            solicitud["deposito"],
            solicitud["tiempo"],
            solicitud["token"],
            solicitud["url"],
        )
    console.print(table)


@app.command()
def crear(
    correo_electronico: str,
    deposito: str,
    token: str,
    url: str,
):
    """
    Crear una solicitud
    """
    rich.print("Crear una solicitud")

    # Validar el correo electrónico
    if not re.match(EMAIL_REGEXP, correo_electronico):
        rich.print("[red]El correo electrónico no es válido[/red]")
        raise typer.Exit(code=1)

    # Validar el URL al archivo PDF
    if not re.match(URL_PDF_FILE_REGEXP, url):
        rich.print("[red]El URL no es válido[/red]")
        raise typer.Exit(code=1)

    # Validar el depósito
    if deposito not in GCS_BUCKETS:
        rich.print("[red]El depósito no existe[/red]")
        raise typer.Exit(code=1)

    # Crear un diccionario con los datos de la solicitud
    solicitud = {
        "correo_electronico": correo_electronico,
        "deposito": deposito,
        "tiempo": datetime.now().isoformat(),
        "token": token,
        "url": url,
    }

    # Guardar la solicitud en la cola
    redis_client.lpush(QUEUE, json.dumps(solicitud))

    # Mensaje de éxito
    rich.print("[green]Solicitud creada[/green]")
    raise typer.Exit(code=0)


@app.command()
def validar():
    """
    Validar solicitudes para crear mensajes
    """
    rich.print("Validar solicitudes para crear mensajes")

    # Obtener y eliminar el primer elemento de la cola
    solicitud_str = redis_client.rpop(QUEUE)

    # Si no hay solicitudes
    if not solicitud_str:
        rich.print("[red]No hay solicitudes[/red]")
        raise typer.Exit(code=0)

    # Preparar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for encabezado in ["Correo electrónico", "Depósito", "Tiempo", "Token", "URL"]:
        table.add_column(encabezado)

    # Bucle por las solicitudes
    while solicitud_str:
        # Cargar datos de la solicitud
        solicitud = json.loads(solicitud_str)

        # Validar el correo electrónico
        if not re.match(EMAIL_REGEXP, solicitud["correo_electronico"]):
            rich.print("[red]El correo electrónico no es válido[/red]")
            continue

        # Validar el URL al archivo PDF
        if not re.match(URL_PDF_FILE_REGEXP, solicitud["url"]):
            rich.print("[red]El URL no es válido[/red]")
            continue

        # Validar el depósito
        if solicitud["deposito"] not in GCS_BUCKETS:
            rich.print("[red]El depósito no existe[/red]")
            continue

        # Agregar una fila a la tabla
        table.add_row(
            solicitud["correo_electronico"],
            solicitud["deposito"],
            solicitud["tiempo"],
            solicitud["token"],
            solicitud["url"],
        )

        # Obtener y eliminar el primer elemento de la cola
        solicitud_str = redis_client.rpop(QUEUE)

    # Mostrar la tabla
    console.print(table)

    # Mensaje de éxito
    rich.print("[green]Solicitudes validadas a mensajes[/green]")
    raise typer.Exit(code=0)


@app.command()
def limpiar():
    """
    Limpiar todas las solicitudes
    """
    rich.print("Limpiar todas las solicitudes")

    # Obtener la cantidad de solicitudes
    count = redis_client.llen(QUEUE)

    # Si no hay solicitudes
    if not count:
        rich.print("[red]No hay solicitudes[/red]")
        raise typer.Exit(code=0)

    # Eliminar todas las solicitudes
    redis_client.delete(QUEUE)

    # Mostrar mensaje de éxito
    rich.print(f"[green]Se eliminaron {count} solicitudes[/green]")
    raise typer.Exit(code=0)
