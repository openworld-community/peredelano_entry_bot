####
FROM python:3.10-slim AS builder

RUN apt-get update -y; \
    apt-get clean && rm -rf /var/lib/apt/lists/*


###
FROM builder AS release

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt; \
    apt-get clean && rm -rf /var/lib/apt/lists/*


COPY . .

CMD [ "python", "run.py" ]
