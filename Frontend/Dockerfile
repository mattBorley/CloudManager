# Step 1: Use an official Node.js image to build the app
FROM node:18 AS builder

# Step 2: Set the working directory inside the container
WORKDIR /AppFrontend

# Step 3: Copy package.json and install dependencies
COPY package*.json .
RUN npm install

# Step 4: Build the app for production
COPY . .
RUN npm run build


# Step 5: Use a lightweight Nginx server to serve the built files
FROM nginx:alpine
COPY --from=builder /AppFrontend/build /usr/share/nginx/html

# Copy the custom Nginx configuration file into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Step 6: Expose port 80 for Nginx
EXPOSE 80

# Step 7: Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]