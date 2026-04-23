FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=Atlantic.settings

# Set the locale
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# es_CO.UTF-8 UTF-8/es_CO.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales
ENV LANG es_CO.UTF-8
ENV LC_ALL es_CO.UTF-8

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN chmod +x /code/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/code/docker-entrypoint.sh"]
CMD ["gunicorn", "Atlantic.wsgi:application", "--bind", "0.0.0.0:8000"]
