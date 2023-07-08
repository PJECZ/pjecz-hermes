"""
Command Line Interface for Hermes
"""
import typer

from hermes.clientes import app as clientes_app
from hermes.depositos import app as depositos_app
from hermes.mensajes import app as mensajes_app
from hermes.solicitudes import app as solicitudes_app

app = typer.Typer()
app.add_typer(clientes_app.app, name="clientes")
app.add_typer(depositos_app.app, name="depositos")
app.add_typer(mensajes_app.app, name="mensajes")
app.add_typer(solicitudes_app.app, name="solicitudes")

if __name__ == "__main__":
    app()
