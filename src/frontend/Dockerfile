# =========================================
# Stage 1: Vite
# =========================================

FROM node:24.12.0-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* ./

RUN --mount=type=cache,target=/root/.npm npm ci

COPY . .

# TODO:
ENV VITE_API_BASE_URL=http://37.205.9.138:8000

RUN npm run build

# =========================================
# Stage 2: Nginx
# =========================================

FROM nginxinc/nginx-unprivileged:alpine3.22

COPY nginx.conf /etc/nginx/nginx.conf

COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

USER nginx

EXPOSE 8080
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
