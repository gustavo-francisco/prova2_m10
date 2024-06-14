FROM python:3.10-alpine
WORKDIR /app
EXPOSE 8080
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["fastapi", "dev", "app.py"]