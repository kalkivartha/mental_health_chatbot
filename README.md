# 🧠 Multilingual Mental Health Chatbot

The **Multilingual Mental Health Chatbot** is a rule-based, voice-enabled conversational agent designed to provide accessible, 24/7 psychological support. Built with Python and Flask, the system uses speech recognition for voice input and integrates the Google Translate API to support communication in multiple languages. This project is optimized for simplicity, cost-effectiveness, and educational use.

---

## 📌 Overview

This chatbot operates on predefined rules and intents, avoiding the complexity and unpredictability of neural network-based models. It offers consistent, fast, and language-independent responses to frequently asked mental health-related queries. The application is particularly suitable for outreach programs, academic projects, or low-resource environments where simplicity and multilingual access are key.

---

## 🔧 Features

| Feature                  | Description                                                              |
| ------------------------ | ------------------------------------------------------------------------ |
| 🌐 Multilingual Support  | Automatically detects and translates messages using Google Translate API |
| 🎤 Voice Input           | Accepts spoken queries via the SpeechRecognition library                 |
| ⚙️ Rule-Based Engine     | Uses intent matching for deterministic, predefined responses             |
| 🕒 24/7 Availability     | Can run continuously for always-on support                               |
| 💰 Cost-Efficient        | Relies entirely on open-source tools and free-tier APIs                  |
| ⚡ Lightweight Deployment | Easy to host on local machines or cloud platforms like Heroku or Render  |

---

## 🛠️ Technology Stack

* **Backend**: Python, Flask
* **Speech Recognition**: `SpeechRecognition` library
* **Translation**: `googletrans==4.0.0-rc1`
* **Logic System**: Rule-based intent mapping
* **Deployment Options**: Heroku, Render, Localhost

---

## 🚀 Installation Guide

### Prerequisites

* Python 3.x installed
* pip (Python package installer)

### Setup Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/mental-health-chatbot.git
   cd mental-health-chatbot
   ```

2. **Install Required Dependencies**

   ```bash
   pip install flask speechrecognition googletrans==4.0.0-rc1
   ```

3. **Run the Application**

   ```bash
   python app.py
   ```

4. **Access the Chatbot**

   * Open a web browser and navigate to: `http://localhost:5000`

---

## 🔄 System Workflow

1. **User Input**: The user submits a message via voice or text.
2. **Language Detection**: The input language is identified.
3. **Translation**: If the message is not in English, it is translated.
4. **Intent Mapping**: The system matches the input to a predefined intent.
5. **Response Generation**: A predefined response is selected and translated back if necessary.
6. **Output**: The reply is returned to the user via text or synthesized voice.

---

## 📂 File Structure

```
mental-health-chatbot/
├── app.py                # Flask application entry point
├── static/               # Static assets (CSS, JS)
├── templates/            # HTML templates for the web UI
├── intents.json          # Predefined intents and responses
└── requirements.txt      # List of dependencies
```

---

## 🤝 Contribution Guidelines

Contributions are encouraged. To contribute:

1. Fork the repository
2. Create a new branch for your feature or fix
3. Submit a pull request with a detailed description of changes

---
## 📜 License

Free to use for educational and personal projects.

---

##  Acknowledgments

* [Flask](https://flask.palletsprojects.com/)
* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
* [googletrans](https://pypi.org/project/googletrans/)

