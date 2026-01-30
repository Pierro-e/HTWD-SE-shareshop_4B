# =========================================
# Stage 1: Vite
# =========================================

FROM node:24.12.0-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* ./

RUN --mount=type=cache,target=/root/.npm npm ci

COPY . .

RUN npm run build

# =========================================
# Stage 2: Nginx
# =========================================

FROM nginx:1.29.4-alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx_default.conf /etc/nginx/conf.d/default.conf

COPY env.sh /docker-entrypoint.d/env.sh
RUN chmod +x /docker-entrypoint.d/env.sh
