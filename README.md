# Custom Chatbot - Ajiz_ChatDuo AI Personal Assistant

Welcome to the **Ajiz_ChatDuo** project! This Python-based personal AI assistant is built using Tkinter for the user interface and offers features like Text-to-Speech (TTS), Wikipedia integration, conversation history storage in SQLite, math calculations, YouTube video playback, website opening, and more.

## Features

### 1. Chat Interface
- **Interactive UI**: Built with Tkinter, the chatbot UI allows users to easily interact with the assistant.
- **Conversation Display**: All chat history is shown in the main chat window.
- **User Input Field**: Users can type their messages and interact with the bot via the input field and send button.

### 2. SQLite Integration
- **Store Conversation History**: The chatbot stores all user-bot interactions in an SQLite database for later retrieval.
- **View/Delete History**: Users can view the chat history or delete it from the app.

### 3. Text-to-Speech (TTS)
- **Pyttsx3 Integration**: The chatbot uses pyttsx3 for Text-to-Speech functionality, making responses more engaging.
- **Custom Greetings**: The bot greets the user based on the time of day (morning, afternoon, or evening).

### 4. Math Calculations
- **Perform Basic Math**: The chatbot can perform basic arithmetic calculations like addition, subtraction, multiplication, and division. For example, you can ask "What is 5 + 7?" and the bot will give the correct answer.

### 5. Play YouTube Videos
- **YouTube Video Playback**: Users can request the chatbot to play any YouTube video by simply providing the title of the video. The bot will use the `pywhatkit` library to open YouTube and start playing the video.

### 6. Open Websites
- **Browse the Web**: The chatbot can open any website for you. Just provide the URL or the website name (e.g., "Open Google"), and it will launch the site in your default web browser.

### 7. Random Responses
- **Motivational Quotes**: The bot can send random motivational thoughts to the user.
- **Fun Facts**: It can also share random fun facts to keep the conversation lively.

### 8. Wikipedia Integration
- **Search Wikipedia**: Users can request information on various topics, and the bot will provide summaries from Wikipedia using the `wikipediaapi` library.

### 9. External Libraries
- **Pywhatkit**: Users can use the bot to play YouTube videos, open websites, or send WhatsApp messages using this library.
- **Threading**: To ensure smooth operation, background tasks (like waiting or TTS) run using Python's threading capabilities.

## Requirements

- Python 3.x
- Tkinter
- Pyttsx3 (Text-to-Speech)
- WikipediaAPI
- Pywhatkit
- SQLite3

You can install the required Python libraries by running:

```bash
pip install pyttsx3 wikipedia-api pywhatkit
