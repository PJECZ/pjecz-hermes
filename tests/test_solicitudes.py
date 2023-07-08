"""
Unit tests for solicitudes
"""
import time

from faker import Faker
from typer.testing import CliRunner

from config.settings import SLEEP
from hermes.app import app

runner = CliRunner()

TOTAL_SOLICITUDES = 5


def test_crear():
    """
    Test crear
    """

    # Probar crear solicitudes
    for _ in range(TOTAL_SOLICITUDES):
        fake = Faker()
        archivo = fake.file_name(extension="pdf")
        correo_electronico = fake.email()
        deposito = fake.bothify(text="???###")
        token = fake.bothify(text="???###")
        result = runner.invoke(
            app,
            [
                "solicitudes",
                "crear",
                archivo,
                correo_electronico,
                deposito,
                token,
            ],
        )
        assert result.exit_code == 0
        assert "Solicitud creada" in result.stdout
        time.sleep(SLEEP)


def test_consultar():
    """
    Test consultar
    """

    # Probar consultar solicitudes
    for _ in range(TOTAL_SOLICITUDES):
        result = runner.invoke(app, ["solicitudes", "consultar"])
        assert result.exit_code == 0
        assert "Consultar solicitudes" in result.stdout
