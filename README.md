# WhatsApp Chat Analyzer

A web application built using Streamlit to analyze WhatsApp chats.

## 🚀 Live Demo
https://whatsappchatanalyser-kycqcdeficat4a5ob7nrod.streamlit.app/



> If the app appears unstyled when opened directly from GitHub, copy the URL above and open it in a new browser tab.

## Features

- 📊 Total messages
- 👥 Most active users
- ☁️ Word cloud
- 🔤 Most common words
- 📅 Monthly timeline
- 📈 Daily timeline
- 🔥 Activity heatmap
- 
WhatsApp Chat Analyzer is a Python-based project that helps to analyze WhatsApp chat data and understand different statistics from a conversation.

The project takes an exported WhatsApp chat file and processes the messages to generate useful information such as total messages, total words, media shared, most active users, and other chat-related statistics.

## Features

- Analyze WhatsApp exported chat files
- Calculate total number of messages
- Calculate total number of words
- Count shared media messages
- Find the most active users
- Analyze user-wise message statistics
- Analyze chat activity over time
- Display statistics using graphs and charts
- Simple and interactive interface using Streamlit

## Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib
- WordCloud
- Regular Expressions (Regex)

## Project Structure

```text
whatsapp_chat_analyser/
│
├── app.py
├── helper.py
├── main.py
├── preprocessor.py
├── stop_hinglish.txt
├── requirements.txt
├── README.md
└── .gitignore

