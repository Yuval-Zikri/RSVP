# Build Stage
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
# Install all dependencies (including dev) for build
# use `npm ci` to respect `package-lock.json` and `--include=dev`
RUN npm ci --legacy-peer-deps --include=dev
COPY . .
RUN npm run build

# Production Stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
