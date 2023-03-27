#!/bin/bash
echo "" > app/crawling.txt
echo "* * * * * /bin/date >> /streamlit/app/log/date-out.log" >> app/crawling.txt
echo "$schedule /usr/local/bin/python3 scrape.py >> /streamlit/app/log/scrape.log" >> app/crawling.txt
crontab app/crawling.txt
cron
python3 app/scrape.py -topic $topic
streamlit run app/sna.py --server.port $port