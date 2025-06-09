FROM python:3.11-slim

# workdir
WORKDIR /app

# OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv==0.7.0

COPY .python-version pyproject.toml uv.lock /app/

# Create a virtual environment and sync dependencies
RUN uv venv 
RUN uv sync --no-install-project

COPY . .
EXPOSE 8000

CMD ["/bin/sh", "-c", ". .venv/bin/activate && mkdocs serve"]