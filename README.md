# pjecz-hermes

Hermes es el encargado de mandar los mensajes con documentos y de llevar una bitácora de destinatarios.

## Instalar software adicional

En Fedora Linux agregue este software

```bash
sudo dnf -y groupinstall "Development Tools"
sudo dnf -y install glibc-langpack-en glibc-langpack-es
sudo dnf -y install pipenv poetry python3-virtualenv
sudo dnf -y install python3-devel python3-docs python3-idle
sudo dnf -y install python3.11
```

## Configuirar Poetry

Por defecto, con **poetry** el entorno se guarda en un directorio en `~/.cache/pypoetry/virtualenvs`

Modifique para que el entorno se guarde en el mismo directorio que el proyecto

```bash
poetry config --list
poetry config virtualenvs.in-project true
```

Verifique que este en True

```bash
poetry config virtualenvs.in-project
```

## Instalar

Clone el repositorio

```bash
cd ~/Documents/GitHub/PJECZ
git clone https://github.com/PJECZ/pjecz-hermes.git
cd pjecz-hermes
```

Instale el entorno virtual con **Python 3.11** y los paquetes necesarios

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install wheel
poetry install
```

## Configurar

Crear un archivo `.env` en la raiz del proyecto con el siguiente contenido:

```ini
# Google Cloud Storage buckets separados por comas
GCS_BUCKETS=

# Plataforma Web API key
PLATAFORMA_WEB_API_URL=http://localhost:8000/v3
PLATAFORMA_WEB_API_KEY=

# Parametros para la API limit, timeout y sleep en segundos
LIMIT=100
TIMEOUT=12
SLEEP=1

# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

# Sendgrid
SENDGRID_API_KEY=
SENDGRID_FROM_EMAIL=
```

Crear un archivo `.bashrc` para activar el entorno virtual y cargar las variables de entorno:

```bash
if [ -f ~/.bashrc ]
then
    . ~/.bashrc
fi

if command -v figlet &> /dev/null
then
    figlet Hermes
else
    echo "== Hermes"
fi
echo

if [ -f .env ]
then
    export $(grep -v '^#' .env | xargs)
    echo "-- Google Cloud Storage buckets"
    echo "   GCS_BUCKETS:            ${GCS_BUCKETS}"
    echo
    echo "-- Requiere arrancar Plataforma Web API key"
    echo "   PLATAFORMA_WEB_API_URL: ${PLATAFORMA_WEB_API_URL}"
    echo "   PLATAFORMA_WEB_API_KEY: ${PLATAFORMA_WEB_API_KEY}"
    echo "   LIMIT:                  ${LIMIT} registros"
    echo "   TIMEOUT:                ${TIMEOUT} segundos"
    echo "   SLEEP:                  ${SLEEP} segundos"
    echo
    echo "-- Requiere arrancar Redis"
    echo "   REDIS_HOST:             ${REDIS_HOST}"
    echo "   REDIS_PORT:             ${REDIS_PORT}"
    echo
    echo "-- Requiere SendGrid para enviar mensajes por correo electrónico"
    echo "   SENDGRID_API_KEY:       ${SENDGRID_API_KEY}"
    echo "   SENDGRID_FROM_EMAIL:    ${SENDGRID_FROM_EMAIL}"
    echo
fi

if [ -d .venv ]
then
    echo "-- Python Virtual Environment"
    source .venv/bin/activate
    echo "   $(python3 --version)"
    export PYTHONPATH=$(pwd)
    echo "   PYTHONPATH: ${PYTHONPATH}"
    echo
    alias cli="python3 ${PWD}/hermes/app.py"
    echo "-- Ejecutar el CLI"
    echo "   cli --help"
    echo
fi
```

## Ejecutar

Ejecute con el alias `cli`

```bash
cli --help
```
