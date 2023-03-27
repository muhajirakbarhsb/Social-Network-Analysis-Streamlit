FROM python:3.9-slim

WORKDIR /streamlit

RUN apt-get update && apt-get install -y \ 
    htop \
    cron \
    vim \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY app/scrape.py app/sna.py datasets/sna.csv app/entry.sh ./app/

ENV port 8051
ENV topic sumbar

RUN pip3 install -r requirements.txt
RUN chmod +x ./app/entry.sh

# EXPOSE $port

# ENTRYPOINT ["streamlit", "run", "app/streamlit.py", "--server.port", port]
ENTRYPOINT ["/streamlit/app/entry.sh"]