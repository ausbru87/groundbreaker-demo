# Using Redhat's RHEL9 Python3.11
FROM registry.access.redhat.com/ubi9/python-311

WORKDIR /app

COPY *.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD [ "python", "/app/app.py"]