# Social-Network-Analysis-Streamlit
# Social-Network-Analysis-Streamlit

This is a Python script that performs social network analysis on Twitter data using the NetworkX and Pyvis libraries. The script uses snscrape to crawl tweets, and is limited to the latest 1500 tweets. The keyword for crawling and the schdule time can be customized in the `docker-compose.yml` file.

## Requirements

- Docker
- Docker Compose

## Installation

Follow the instructions below to run the example:

1. **Install Docker** if you haven't used it before. 

2. **Clone** the repository:
```bash
git clone https://github.com/muhajirakbarhsb/Social-Network-Analysis-Streamlit.git
```

3. **Change directory**:
```bash
cd Social-Network-Analysis-Streamlit
```
4. **Start the Docker containers**:
```bash
docker-compose up -d
```

## Usage

Customize the `docker-compose.yml` file with your desired **keyword** and **time** to schedule:
```bash
    environment:
      port: "8543"
      topic: "sumbar"
      schedule: "30 * * * *"
```
The services will be available in your system:
1. Streamlit Dashboard at port 8543
2. Twitter Crawler `app/scrape.py`

**Stop** the Docker Containers.
```bash
docker-compose down
```
