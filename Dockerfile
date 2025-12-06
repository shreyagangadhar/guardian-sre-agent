FROM python:3.9-slim

# Install system dependencies (used by psutil or other tools if needed)
RUN apt-get update && apt-get install -y procps net-tools && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the dashboard port
EXPOSE 5001

# Use the shell script as entrypoint to run both processes
CMD ["bash", "render_build.sh"]
