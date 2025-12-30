FROM python:3.11-slim
WORKDIR /app
# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Run tests
CMD ["python", "-m", "pytest", "test_csv.py", "-v"]
