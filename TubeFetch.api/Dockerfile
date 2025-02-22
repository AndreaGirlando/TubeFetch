FROM ubuntu:latest

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv ffmpeg \
    && apt-get clean
RUN apt-get install -y libpq-dev
RUN python3 -m pip install --no-cache-dir -r requirements.txt --break-system-packages
RUN pip install yt-dlp -U --break-system-packages

EXPOSE 5000

CMD ["python3", "-m", "api", "run", "--host=0.0.0.0", "--port=5000"]

