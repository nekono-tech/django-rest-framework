FROM node:20.16.0-bullseye

WORKDIR /app

COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm npm install

COPY . .

CMD ["npm", "run", "dev"]
