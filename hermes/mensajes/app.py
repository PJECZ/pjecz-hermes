"""
CLI Mensajes

Un mensaje fue una solicitud que cumplió con los requisitos y que espera ser enviado.

"""
import json

import rich
import typer

from lib.redis import redis_client

QUEUE = "hermes_mensajes"

app = typer.Typer()


@app.command()
def consultar():
    """
    Consultar mensajes
    """
    rich.print("Consultar mensajes")

    # Obtener y eliminar el primer elemento de la cola
    mensaje_str = redis_client.rpop(QUEUE)

    # Si no hay mensajes
    if not mensaje_str:
        rich.print("[red]No hay mensajes[/red]")
        raise typer.Exit(code=0)

    # Mostrar los datos del mensaje
    mensaje = json.loads(mensaje_str)
    rich.print(f"Archivo: {mensaje['archivo']}")
    rich.print(f"Correo electrónico: {mensaje['correo_electronico']}")
    rich.print(f"Depósito: {mensaje['deposito']}")
    rich.print(f"Token: {mensaje['token']}")
    raise typer.Exit(code=0)


@app.command()
def crear(
    archivo: str,
    correo_electronico: str,
    deposito: str,
    token: str,
):
    """
    Crear un mensaje
    """
    rich.print("Crear un mensaje")

    # Crear un diccionario con los datos del mensaje
    mensaje = {
        "archivo": archivo,
        "correo_electronico": correo_electronico,
        "deposito": deposito,
        "token": token,
    }

    # Guardar el mensaje en la cola
    redis_client.lpush(QUEUE, json.dumps(mensaje))

    # Mostrar mensaje de éxito
    rich.print("[green]Mensaje creado[/green]")
