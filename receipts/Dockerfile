FROM node:18-slim
WORKDIR /app
RUN npm init -y && npm install \
    express \
    @opentelemetry/sdk-node \
    @opentelemetry/auto-instrumentations-node \
    @opentelemetry/exporter-otlp-http
COPY index.js .
EXPOSE 3000
CMD ["node", "--require", "@opentelemetry/auto-instrumentations-node/register", "index.js"]