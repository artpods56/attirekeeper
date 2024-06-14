FROM nvidia/cuda:12.1.0-devel-ubuntu20.04

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y python3-pip apt-utils
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN ln -s /usr/bin/python3 /usr/bin/python

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
