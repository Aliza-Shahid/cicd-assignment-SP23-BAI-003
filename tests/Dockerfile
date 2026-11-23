FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir selenium pytest

WORKDIR /app
COPY test_site.py /app/test_site.py

CMD ["pytest", "-v", "--junitxml=/app/reports/results.xml", "/app/test_site.py"]