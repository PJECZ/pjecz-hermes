"""
CLI Mensajes

Un mensaje fue una solicitud que cumplió con los requisitos y que espera ser enviada.

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
    rich.print(f"Correo electrónico: {mensaje['correo_electronico']}")
    rich.print(f"Depósito: {mensaje['deposito']}")
    rich.print(f"Estado: {mensaje['estado']}")
    rich.print(f"Token: {mensaje['token']}")
    rich.print(f"URL: {mensaje['url']}")
    raise typer.Exit(code=0)


@app.command()
def crear(
    correo_electronico: str,
    deposito: str,
    token: str,
    url: str,
):
    """
    Crear un mensaje
    """
    rich.print("Crear un mensaje")

    # Crear un diccionario con los datos del mensaje
    mensaje = {
        "correo_electronico": correo_electronico,
        "deposito": deposito,
        "estado": "PENDIENTE",
        "token": token,
        "url": url,
    }

    # Guardar el mensaje en la cola
    redis_client.lpush(QUEUE, json.dumps(mensaje))

    # Mostrar mensaje de éxito
    rich.print("[green]Mensaje creado[/green]")


@app.command()
def enviar():
    """
    Enviar los mensajes pendientes
    """
    rich.print("Enviar los mensajes pendientes")

    # Obtener todos los mensajes pendientes
    mensajes = redis_client.lrange(QUEUE, 0, -1)

    # Si no hay mensajes
    if not mensajes:
        rich.print("[red]No hay mensajes[/red]")
        raise typer.Exit(code=0)

    # Bucle con los mensajes
    for mensaje_str in mensajes:
        mensaje = json.loads(mensaje_str)
        rich.print(f"Para {mensaje['correo_electronico']}")
        rich.print(f"Asunto: Archivo que solicitaste")
        rich.print(f"Contenido: Buen día, aquí está el archivo que solicitaste: {mensaje['url']}")
        rich.print("")
