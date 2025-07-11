# Use the official Python image as a base
FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Build the application
RUN python manage.py collectstatic --noinput

# Final stage to create a lightweight image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the built application from the builder stage
COPY --from=builder /app /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
