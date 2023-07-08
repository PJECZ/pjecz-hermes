"""
CLI Clientes

Un cliente es una persona a la que ya se le ha enviado un mensaje o más.

Se va a recordar

- Su correo electrónico
- La cantidad de descargas que ha realizado

"""
import json

import rich
import typer

from lib.redis import redis_client

QUEUE = "hermes_clientes"

app = typer.Typer()


@app.command()
def consultar():
    """
    Consultar clientes
    """
    rich.print("Consultar clientes")

    # Obtener y eliminar el primer elemento de la cola
    cliente_str = redis_client.rpop(QUEUE)

    # Si no hay clientes
    if not cliente_str:
        rich.print("[red]No hay clientes[/red]")
        raise typer.Exit(code=0)

    # Mostrar los datos del cliente
    cliente = json.loads(cliente_str)
    rich.print(f"Correo electrónico: {cliente['correo_electronico']}")
    rich.print(f"Descargas: {cliente['descargas']}")
    raise typer.Exit(code=0)


@app.command()
def crear(
    correo_electronico: str,
    descargas: int,
):
    """
    Crear un cliente
    """
    rich.print("Crear un cliente")

    # Crear un diccionario con los datos del cliente
    cliente = {
        "correo_electronico": correo_electronico,
        "descargas": descargas,
    }

    # Guardar el cliente en la cola
    redis_client.lpush(QUEUE, json.dumps(cliente))

    # Mensaje de éxito
    rich.print("[green]Cliente creado[/green]")
    raise typer.Exit(code=0)
