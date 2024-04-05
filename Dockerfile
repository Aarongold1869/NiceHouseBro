FROM python:3

WORKDIR /NiceHouseBro

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN curl -s https://get.modular.com | sh -
    && modular install mojo

ARG MODULAR_HOME="/root/.modular"
ENV MODULAR_HOME=$MODULAR_HOME  
ENV PATH="$PATH:/$MODULAR_HOME/pkg/packages.modular.com_mojo/bin"

COPY . .
RUN mojo property/functions/cap_rate.mojo
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

ARG PORT=8000
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]