FROM python:3.13-slim AS base

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
COPY repo/hololinked /app/repo/hololinked
RUN uv venv
RUN uv sync --no-install-project --no-default-groups --group repo

COPY . .

# development image
FROM base AS dev
# ARG MKDOCS_DIRTY_RELOAD=false
# unfortunately dirty reloading is not fast, so we skip now
EXPOSE 8000
CMD ["/bin/sh", "-c", ". .venv/bin/activate && mkdocs serve -a 0.0.0.0:8000"]

# production image
FROM base AS build
RUN . .venv/bin/activate && mkdocs build

FROM nginx:alpine AS prod
COPY --from=build /app/site /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
