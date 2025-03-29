FROM python:3.10

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Run the FastAPI app on port 3000 inside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
