FROM python:3
COPY . /discord-bot
WORKDIR /discord-bot

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "DiscordBot.py"]
