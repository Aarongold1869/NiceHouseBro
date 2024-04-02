FROM python:3

WORKDIR /NiceHouseBro

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

ARG PORT=8000
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]