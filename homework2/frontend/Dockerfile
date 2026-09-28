FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
COPY src ./src
COPY index.html ./
COPY vite.config.js ./
RUN npm ci
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=10s --timeout=3s --retries=3 CMD wget --no-verbose --tries=1 --spider http://127.0.0.1/ || exit 1
