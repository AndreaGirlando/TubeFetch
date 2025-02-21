FROM ubuntu:latest

WORKDIR /usr/src/app

COPY . /usr/src/app

# Installa Python, pip, venv e ffmpeg
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv ffmpeg \
    && apt-get clean
RUN apt-get install -y libpq-dev
# Installa le dipendenze di Python
RUN python3 -m pip install --no-cache-dir -r requirements.txt --break-system-packages

EXPOSE 5000

CMD ["python3", "-m", "api", "run", "--host=0.0.0.0", "--port=5000"]

