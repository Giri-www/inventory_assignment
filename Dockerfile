FROM python

RUN apt update


ARG PROJECT=inventory_proj
ARG PROJECT_DIR=/home/ubuntu/inventory_proj/

WORKDIR $PROJECT_DIR

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ADD . $PROJECT_DIR

ENTRYPOINT [ "python3", "manage.py" ]

CMD [ "runserver", "0.0.0.0:8000" ]