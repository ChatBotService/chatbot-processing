FROM python:3-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
#RUN pip uninstall -r requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8083
CMD [ "python", "./run.py" ]

# docker rmi $(docker images -a -q) -f

# docker run --netowrk --name some-postgres -e POSTGRES_PASSWORD=123 -d postgres