# =========================================
# Configurations
# =========================================

ARG PYTHON_VERSION=3.14.2-slim
ARG DB_NAME=share_shop
ARG DB_USER=userAdmin
ARG DB_PASSWORD=xdb_Admin890!
ARG DB_HOST=localhost

# =========================================
# Stage 1: Build and Serve
# =========================================

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}

WORKDIR /app

ARG UID=10001

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

USER appuser

COPY . .

EXPOSE 8000

CMD uvicorn 'share_shop_api:app' --host=0.0.0.0 --port=8000
