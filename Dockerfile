FROM python:3.10
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . .
RUN pip install -r requirments.txt
RUN echo "Package Installation done"
EXPOSE 80
CMD ["python3", "manage.py", "runserver","0.0.0.0:80"]