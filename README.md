
# Screen Translator (ScreenTL)

Screen Translator (ScreenTL) is a desktop application that captures a selected screen area, performs OCR (Optical Character Recognition) on the captured image, and translates the recognized text into a target language. It can also function as a standalone text translator, similar to Google Translate.

## ✨ Features

- 🖼️ **GUI with Tkinter** – User-friendly interface for easy interaction  
- 🔤 **OCR Options**:
  - [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) – supports 41 languages
  - **Google Cloud Vision API** – supports broader language coverage
- 🌐 **Translation Options**:
  - [Deep Translator](https://github.com/nidhaloff/deep-translator) (Google Translate engine)
  - **Google Cloud Translation API v3**
- 🗃️ **Translation History Tracking** using **SQLite** database
- 📈 **History & API Usage Viewer** built with Streamlit
- ✅ Cross-platform support (Windows tested)

## 🛠️ Tech Stack

- Python 3.12
- Tkinter (GUI)
- PaddleOCR
- Google Cloud APIs (Vision & Translation)
- Deep Translator
- SQLite (for local database)
- Streamlit

## 🚀 Getting Started

1. **Clone the repository**
  ```bash
  git clone https://github.com/Nevaraay/ScreenTL.git
  cd ScreenTL
  ```

2. **Install dependencies using conda**
  ```bash
  conda env create -f environment.yml
  conda activate nevar
  ```

3. **Run the app**
  ```bash
  python main.py
  ```