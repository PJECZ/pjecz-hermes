"""
CLI Solicitudes

Una solicitud es una petición de un cliente para descargar un archivo.

Son creadas por plataforma-web-api-new directamente en Redis.

Se validan los campos y si cumple con los requisitos se converten en Mensajes.

"""
import json

import rich
import typer

from lib.redis import redis_client

QUEUE = "hermes_solicitudes"

app = typer.Typer()


@app.command()
def consultar():
    """
    Consultar solicitudes
    """
    rich.print("Consultar solicitudes")

    # Obtener y eliminar el primer elemento de la cola
    solicitud_str = redis_client.rpop(QUEUE)

    # Si no hay solicitudes
    if not solicitud_str:
        rich.print("[red]No hay solicitudes[/red]")
        raise typer.Exit(code=0)

    # Mostrar los datos de la solicitud
    solicitud = json.loads(solicitud_str)
    rich.print(f"Archivo: {solicitud['archivo']}")
    rich.print(f"Correo electrónico: {solicitud['correo_electronico']}")
    rich.print(f"Depósito: {solicitud['deposito']}")
    rich.print(f"Token: {solicitud['token']}")
    raise typer.Exit(code=0)


@app.command()
def crear(
    archivo: str,
    correo_electronico: str,
    deposito: str,
    token: str,
):
    """
    Crear una solicitud
    """
    rich.print("Crear una solicitud")

    # Crear un diccionario con los datos de la solicitud
    solicitud = {
        "archivo": archivo,
        "correo_electronico": correo_electronico,
        "deposito": deposito,
        "token": token,
    }

    # Guardar la solicitud en la cola
    redis_client.lpush(QUEUE, json.dumps(solicitud))

    # Mensaje de éxito
    rich.print("[green]Solicitud creada[/green]")
    raise typer.Exit(code=0)
