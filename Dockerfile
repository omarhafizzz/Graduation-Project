FROM python:3.11-slim

# working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Install supervisor to run multiple processes
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Supervisor config to run both Flask and sender
RUN echo "[supervisord]\nnodaemon=true\n\
[program:flask]\ncommand=python app.py\nautostart=true\nautorestart=true\nstdout_logfile=/dev/stdout\nstdout_logfile_maxbytes=0\nstderr_logfile=/dev/stderr\nstderr_logfile_maxbytes=0\n\
[program:sender]\ncommand=python sender.py\nautostart=true\nautorestart=true\nstartsecs=3\nstdout_logfile=/dev/stdout\nstdout_logfile_maxbytes=0\nstderr_logfile=/dev/stderr\nstderr_logfile_maxbytes=0" \
> /etc/supervisor/conf.d/electravision.conf

EXPOSE 5000

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]