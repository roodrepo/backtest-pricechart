FROM python:3.8-alpine3.14

RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update
RUN apk add --update --no-cache python3 python3-dev mariadb-dev build-base libffi-dev gcc g++ musl-dev linux-headers npm netcat-openbsd git py3-numpy
RUN pip install --upgrade pip
RUN pip install pandas-ta

RUN apk add --update --no-cache libpng-dev libgcc libquadmath libgfortran libexecinfo-dev openblas-dev lapack-dev libgomp llvm11-dev

COPY ./app/requirements.txt /app/

RUN pip install -r /app/requirements.txt --no-cache-dir

RUN adduser --disabled-password --no-create-home app
RUN mkdir -p /vol/web/static
RUN mkdir -p /vol/web/media
RUN chown -R app:app /vol
RUN chmod -R 755 /vol

COPY ./app /app
WORKDIR /app

ENV PATH="/app/scripts-shell:/py/bin:$PATH"
CMD ["scripts-shell/wait.sh"]