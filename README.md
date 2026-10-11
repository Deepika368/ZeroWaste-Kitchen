# 🥗 ZeroWaste Kitchen — Food Planning AI Agent

## About the Project

ZeroWaste Kitchen is an AI-powered food planning application built with Python and Streamlit. It helps users manage kitchen ingredients, monitor expiry dates, generate meal suggestions, and reduce food waste.

## Features

* 🥕 Ingredient inventory management
* ⏰ Expiry date alerts
* 🤖 AI-powered meal planning using Google Gemini
* 🛒 Shopping list management
* 📥 Downloadable shopping list
* 📊 Kitchen dashboard

## Technologies Used

* Python
* Streamlit
* Google Gemini API
* Pandas
* Python dotenv

## Project Structure

```text
ZeroWaste-Kitchen/
├── app.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

**Note:** Keep `.env` private. Do not upload your API key to GitHub.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Deepika368/ZeroWaste-Kitchen.git
cd ZeroWaste-Kitchen
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment on Windows

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Create a `.env` file in the project folder and add:

```text
GEMINI_API_KEY=your_api_key_here
```

Replace the example value with your actual API key. Never commit this file to GitHub.

### 6. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal.

## Future Enhancements

* Persistent storage using SQLite
* Automated expiry notifications
* Weekly meal planning
* Food waste and savings analytics
* Personalized recipe recommendations

## Project Goal

To encourage sustainable cooking by helping households plan meals efficiently, use available ingredients, and reduce avoidable food waste.

## Author

Developed as an AI agent project using Python and generative AI.
