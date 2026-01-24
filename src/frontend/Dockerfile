# =========================================
# Configurations
# =========================================

ARG NODE_VERSION=24.12.0-alpine
ARG NGINX_VERSION=alpine3.22
ARG API_BASE_URL=http://37.205.9.138:8000

# =========================================
# Stage 1: Build
# =========================================

FROM node:${NODE_VERSION} AS builder

WORKDIR /app

COPY package.json package-lock.json* ./

RUN --mount=type=cache,target=/root/.npm npm ci

COPY . .

ARG API_BASE_URL
ENV VITE_API_BASE_URL=${API_BASE_URL}

RUN npm run build

# =========================================
# Stage 2: Serve
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION}

COPY nginx.conf /etc/nginx/nginx.conf

COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

USER nginx

EXPOSE 8080

ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
