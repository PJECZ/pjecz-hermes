"""
CLI Solicitudes
"""
import json

import rich
import typer

app = typer.Typer()

from lib.redis import redis_client

QUEUE = "hermes_solicitudes"


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

    # Terminar con codigo de salida cero
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

    # Guardar la solicitud en Redis
    redis_client.lpush(QUEUE, json.dumps(solicitud))

    # Mensaje de confirmación
    rich.print("[green]Solicitud creada[/green]")

    # Terminar con codigo de salida cero
    raise typer.Exit(code=0)
