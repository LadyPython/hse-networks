FROM python
RUN apt-get update && apt-get install -y iputils-ping

WORKDIR /usr/src/script

RUN pip3 install click

COPY . .

ENTRYPOINT ["python3", "-u", "find_mtu.py"]
