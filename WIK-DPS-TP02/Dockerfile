FROM python:3.12-slim
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
RUN pip install --no-cache-dir fastapi uvicorn
WORKDIR /app
COPY tp.py .
RUN chown -R appuser:appgroup /app
USER appuser
EXPOSE 8080 8081
CMD ["python", "tp.py"]
