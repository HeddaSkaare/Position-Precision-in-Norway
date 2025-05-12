FROM python:3.11

# Sett arbeidsmappe
WORKDIR /app

# Kopier prosjektfilene
COPY . /app

# Installer avhengigheter
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Eksponer port (hvis Flask kjører på 5000)
EXPOSE 5000

# Start appen (bruk gunicorn i produksjon!)
CMD ["gunicorn", "--worker-class", "gevent", "--timeout", "300", "-b", "0.0.0.0:5000", "app:app"]

