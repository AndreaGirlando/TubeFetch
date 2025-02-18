FROM ubuntu:latest

WORKDIR /usr/src/app

COPY . /usr/src/app

# Installa Python, pip, venv e ffmpeg
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv ffmpeg \
    && apt-get clean

# Aggiorna pip usando apt invece di pip install --upgrade
RUN apt-get install -y python3-pip --only-upgrade

# Installa le dipendenze di Python
RUN python3 -m pip install --no-cache-dir -r requirements.txt --break-system-packages

# Imposta la variabile d'ambiente per Flask
ENV FLASK_APP=api

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
