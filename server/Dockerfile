from python:3.7

RUN pip install Flask gunicorn

COPY src/ app/
WORKDIR /app

ENV PORT 8080

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]