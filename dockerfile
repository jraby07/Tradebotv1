FROM python:3.10-slim
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "webapp.py"]

CMD ["python", "webapp.py"]


