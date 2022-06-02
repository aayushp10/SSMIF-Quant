# Specifies where to get the base image (Node v15 in our case) and creates a new container for it
FROM node:15

# Set working directory. Paths will be relative this WORKDIR.
WORKDIR /usr/src/app

# Install dependencies
COPY package.json ./
COPY yarn.lock ./
RUN yarn install

# Copy source files from host computer to the container
COPY . .

# Specify port app runs on
EXPOSE 3000

# Run the app
CMD [ "yarn", "start" ]
