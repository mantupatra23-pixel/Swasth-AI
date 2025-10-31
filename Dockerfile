FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
RUN apt-get update && apt-get install -y ffmpeg
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
