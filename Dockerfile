FROM python:3.6.10
COPY . /var/app/
WORKDIR /var/app

RUN chmod +x /var/app/run.sh
RUN pip install -r requirements.txt --no-cache-dir

CMD ["/bin/bash", "./run.sh"]