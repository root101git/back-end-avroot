FROM python:3.11.3-slim
WORKDIR /backend

COPY . /backend
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8080
CMD [ "uvicorn","main:app","--reload","--host","0.0.0.0","--port","8080" ]
