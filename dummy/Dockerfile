FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn opentelemetry-distro opentelemetry-exporter-otlp
RUN opentelemetry-bootstrap -a install
COPY api_hit.py .
EXPOSE 9000
CMD ["opentelemetry-instrument", "uvicorn", "api_hit:app", "--host", "0.0.0.0", "--port", "9000"]