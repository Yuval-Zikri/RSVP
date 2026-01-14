# Build Stage
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
ENV NPM_CONFIG_PRODUCTION=false
RUN npm install --legacy-peer-deps --include=dev
COPY . .
RUN chmod -R +x node_modules/.bin
RUN ls -la node_modules || true
RUN ls -la node_modules/.bin || true
RUN node -v && npm -v
RUN npm install -g vite
RUN npm run build

# Production Stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
