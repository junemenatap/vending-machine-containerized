FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn
COPY api_hit.py .
EXPOSE 9000
CMD ["uvicorn", "api_hit:app", "--host", "0.0.0.0", "--port", "9000"]