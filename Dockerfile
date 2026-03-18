# 1. Use an official Python image
FROM python:3.11-slim

# 2. Set the "home" folder inside the container
WORKDIR /app

# 3. Copy the list of libraries first (better for caching)
COPY requirements.txt .

# 4. Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all your code into the container
COPY . .

# 6. Open the port FastAPI uses
EXPOSE 8000

# 7. Command to start the app
CMD ["uvicorn", "vending_machine:app", "--host", "0.0.0.0", "--port", "8000"]