FROM python:3.7
COPY . /discord-bot
WORKDIR /discord-bot

RUN apt-get update
RUN apt-get install -y ffmpeg
RUN python3 -m pip install -r requirements.txt

CMD ["python3", "DiscordBot.py"]
