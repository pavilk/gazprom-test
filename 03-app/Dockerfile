FROM python:3.14-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --system --no-create-home --shell /usr/sbin/nologin app

WORKDIR /opt/hello-app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

USER app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
