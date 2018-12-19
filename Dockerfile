# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.6
# copy current folder (.) into container folder /app
COPY . /app
# set the working directory as /app
WORKDIR /app
# install requirements with pip install
RUN pip install -r requirements.txt
# run the file with python app.py
ENTRYPOINT ["python"]
CMD ["app.py"]
