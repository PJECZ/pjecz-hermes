"""
Unit tests for solicitudes
"""
import random
import time

from faker import Faker
from typer.testing import CliRunner

from config.settings import GCS_BUCKETS, SLEEP
from hermes.app import app

runner = CliRunner()


def test_crear():
    """
    Test crear
    """

    # Definir una cantidad de solicitude a crear de 1 a 10
    total_solicitudes = random.randint(1, 10)

    # Crear un objeto Faker
    fake = Faker()

    # Crear solicitudes
    for _ in range(total_solicitudes):
        # Definir un depósito aleatorio
        deposito = random.choice(GCS_BUCKETS)

        # Definir los parametros
        correo_electronico = fake.email()
        token = fake.bothify(text="???###")
        url = f"https://storage.googleapis.com/{deposito}/{fake.file_name(extension='pdf')}"

        # Ejecutar el comando para crear una solicitud
        result = runner.invoke(
            app,
            [
                "solicitudes",
                "crear",
                correo_electronico,
                deposito,
                token,
                url,
            ],
        )
        assert result.exit_code == 0
        assert "Solicitud creada" in result.stdout
        time.sleep(SLEEP)
