"""
CLI Clientes
"""
import rich
import typer

app = typer.Typer()


@app.command()
def consultar():
    """
    Consultar clientes
    """
    rich.print("Consultar clientes")
