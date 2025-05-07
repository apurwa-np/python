FROM python:3.9-slim

# Create a non-root user and group
RUN addgroup --system flaskgroup && adduser --system --ingroup flaskgroup flaskuser

# Set workdir and copy code
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r pyreq.txt

# Change ownership of the app directory to the non-root user
RUN chown -R flaskuser:flaskgroup /app

# Switch to non-root user
USER flaskuser

# Run the app
CMD ["python", "app.py"]