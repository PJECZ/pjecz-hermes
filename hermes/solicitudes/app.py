"""
CLI Solicitudes

Una solicitud es una petición de un cliente para descargar un archivo.

Son creadas por plataforma-web-api-new directamente en Redis.

Se validan los campos y si cumple con los requisitos se converten en Mensajes.

"""
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

    # Bucle por las solicitudes
    while solicitud_str:
        # Cargar datos de la solicitud
        solicitud = json.loads(solicitud_str)

        # Mostrar sus datos
        rich.print(f"Correo electrónico: {solicitud['correo_electronico']}")
        rich.print(f"Depósito: {solicitud['deposito']}")
        rich.print(f"Token: {solicitud['token']}")
        rich.print(f"URL: {solicitud['url']}")
        rich.print("")

        # Obtener y eliminar el primer elemento de la cola
        solicitud_str = redis_client.rpop(QUEUE)

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
