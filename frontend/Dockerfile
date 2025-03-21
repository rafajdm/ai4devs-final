# Stage 1: Build the application
FROM node:20 as builder

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy the rest of the application and build it with Vite
COPY . ./
RUN npm run build

# Stage 2: Serve the built application using nginx
FROM nginx:1.21-alpine

# Copy the build output from the builder stage to nginx's html directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 for serving the application
EXPOSE 8080

# Start nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]