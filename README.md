<h1 align="center">Instant Answers GPT Bot</h1>

<h2 align="center">This is a Telegram bot that provides instant answers using OpenAI Assistants Stream.</h2>
<div align="center"><img src="instant.gif" alt="instant" height="1020" width="522"></div>

## Features:
- Quick and stream responses to user queries.
- Integrated with MongoDB + Beanie ODM for data persistence.

## Installation:
1. ### Clone the repository:
   ```bash
   git clone https://github.com/west3n/instant-answers-gpt-bot.git
   cd instant-answers-gpt-bot

2. ### Rename .env.example to .env and fill it with your data:

- BOT_TOKEN: Telegram API token. [How to grab it](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)
- OPENAI_API_KEY: OpenAI API Key. [How to grab it](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)

3. ### Build the Docker image and start the containers:
   ```bash
   docker-compose up --build
