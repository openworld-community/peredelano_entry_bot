####
FROM python:3.10-slim AS builder

RUN apt-get update -y; \
    apt-get clean && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt .

# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --requirement requirements.txt; \
       apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["python", "run.py"]

####
FROM builder AS release

COPY . .
EXPOSE 80

STOPSIGNAL SIGQUIT
CMD ["python", "run.py"]

