# Build stage
FROM node:20-alpine AS build
# Default empty — production builds use relative /api/* URLs (frontend nginx
# proxies them to per-customer backend via Docker network). DEPTEST and
# standalone deploys override with --build-arg VITE_API_URL=http://...
ARG VITE_API_URL=
ENV VITE_API_URL=${VITE_API_URL}
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
# Host MUST generate src/version.ts before docker build (no .git in context);
# version.cjs gracefully preserves existing src/version.ts when run inside container.
RUN npm run build

# Serve stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -q -O - http://127.0.0.1/ > /dev/null || exit 1
