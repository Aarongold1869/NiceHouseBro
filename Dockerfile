FROM python:3

WORKDIR /NiceHouseBro

#give ARG RAILS_ENV a default value = production
ARG DJANGO_SECRET=(pbga&v@c75)ya%r5^9q3=ehyl#&=8dd(%p_6qf(411&n#$v5b
ARG SERVER=PROD

#assign the $RAILS_ENV arg to the RAILS_ENV ENV so that it can be accessed
#by the subsequent RUN call within the container
ENV DJANGO_SECRET $DJANGO_SECRET
ENV SERVER $SERVER

#the subsequent RUN call accesses the RAILS_ENV ENV variable within the container
RUN if [ "$SERVER" = "PROD" ] ; then echo "production env"; else echo "non-production env: $SERVER"; fi

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

ARG PORT=8000
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]