# Use Node.js 18 on Alpine Linux (Lightweight)
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files first (better caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the code
COPY . .

# Expose the Vite port
EXPOSE 5173

# Start the app with "--host" so it's accessible outside the container
CMD ["npm", "run", "dev", "--", "--host"]