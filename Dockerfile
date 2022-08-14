# syntax=docker/dockerfile:1

# 
FROM python:3.10

# 
WORKDIR /Dock

# 
COPY ./requirements.txt /Dock/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /Dock/requirements.txt

# 
COPY ./main.py /Dock/

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
