# Step 1: Use an official Node.js image to build the app
FROM node:18 AS builder

# Step 2: Set the working directory inside the container
WORKDIR /AppFrontend

# Step 3: Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Step 4: Copy the rest of the React app source code
COPY . .

# Step 5: Build the app for production
RUN npm run build

# Step 6: Use a lightweight Nginx server to serve the built files
FROM nginx:alpine
COPY --from=builder /AppFrontend/build /usr/share/nginx/html

# Step 7: Expose port 80 and define the entry point
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
