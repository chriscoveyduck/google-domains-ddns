FROM python:3

RUN adduser -D worker
USER worker
WORKDIR /home/worker

COPY --chown=worker:worker requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt

ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker . .

LABEL maintainer="Chris Coveyduck <chris@anthillmob.net>" \
      version="1.0.0"

CMD [ "python", "./main.py" ]