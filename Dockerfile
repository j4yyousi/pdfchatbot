FROM python:3.13-slim

#RUN python -m venv /venv
#ENV PATH="/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

#COPY . /pdfchatbot

# Create the app directory
RUN mkdir /pdfchatbot

RUN useradd -m -r appuser && \
    chown -R appuser /pdfchatbot

# Set the working directory
WORKDIR /pdfchatbot
 
COPY --chown=appuser:appuser . .

USER appuser

#in case we have static files
RUN python manage.py collectstatic

EXPOSE 8000 

CMD ["gunicorn", "--bind", ":8000", "pdfchatbot.wsgi:application"] 