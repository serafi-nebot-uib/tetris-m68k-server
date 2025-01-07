from python:3.13-slim
workdir /app
copy . /app
run pip install -r requirements.txt
expose 6969
entrypoint ["python", "server.py"]
