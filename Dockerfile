FROM python:3.8.2
WORKDIR /src
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
ENV IN_DOCKER=1
EXPOSE 5000
CMD [ "python3","-u", "main.py" ]