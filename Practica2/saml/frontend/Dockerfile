FROM node:20-alpine

WORKDIR /app

# Copy dependency specifications
COPY package*.json ./

# Install npm packages
RUN npm install

# Copy code and configs
COPY . .

# Expose port
EXPOSE 3001

# Run in development mode
CMD ["npm", "run", "dev"]
