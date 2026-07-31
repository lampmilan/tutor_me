# Isolated Python runner for student code
FROM python:3.12-slim

WORKDIR /workspace

# No network tools; minimal surface
RUN useradd -m -u 1000 student && chown -R student:student /workspace

USER student

CMD ["python", "main.py"]
