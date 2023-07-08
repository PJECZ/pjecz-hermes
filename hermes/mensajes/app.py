"""
CLI Mensajes
"""
import rich
import typer

app = typer.Typer()


@app.command()
def consultar():
    """
    Consultar mensajes
    """
    rich.print("Consultar mensajes")
