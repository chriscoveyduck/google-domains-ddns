FROM python:3.8-buster

RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser

COPY --chown=appuser:appuser requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt

ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=appuser:appuser . .

LABEL maintainer="Chris Coveyduck <chris@anthillmob.net>" \
      version="1.0.0"

CMD [ "python", "./main.py" ]