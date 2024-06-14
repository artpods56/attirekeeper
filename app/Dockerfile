FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

COPY . .

COPY ./entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

RUN echo "Excute the entrypoint.sh script"
ENTRYPOINT ["bash", "/code/entrypoint.sh"]

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
