FROM python:3.11

WORKDIR /code

COPY .requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

EXPOSE 8001
# Assuming the correct Docker tools are in a local directory named 'docker-tools'
#COPY ../docker-tools/ /usr/local/bin/

EXPOSE 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
