FROM python:3.8 as base

FROM base as install_deps

# Install requirements in the 'install_deps' phase
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt
  
FROM base as application

# Copy installed packages in 'application' phase
COPY --from=install_deps /install /usr/local

COPY ./app /app

WORKDIR /app

CMD ["python", "trade_bot.py"]
