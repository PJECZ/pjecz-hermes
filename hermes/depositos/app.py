"""
CLI Depositos
"""
import rich
import typer

from config.settings import GCS_BUCKETS

app = typer.Typer()


@app.command()
def consultar():
    """
    Consultar depositos
    """
    rich.print("Consultar depositos")

    # Mostrar Google Cloud Storage buckets
    for bucket in GCS_BUCKETS:
        rich.print(bucket)
