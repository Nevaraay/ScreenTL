
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

2. **Install dependencies**
   - Using pip:
     ```bash
     pip install -r requirements.txt
     ```
   - Or using Conda:
     ```bash
     conda env create -f environment.yml
     conda activate nevar
     ```

3. **Run the app**
   ```bash
   python main.py
   ```

> The project is modularized into multiple Python scripts, with `main.py` as the entry point.

## ⚠️ Limitations

- PaddleOCR currently supports only 41 languages, so the available translation targets are limited to those languages. [See supported languages](https://www.paddleocr.ai/latest/en/version3.x/algorithm/PP-OCRv5/PP-OCRv5_multi_languages.html#3-performance-comparison)
- Requires Google Cloud credentials if using Google APIs (Vision or Translate).
  - Specifically, you must place your **Google service account JSON key** (e.g., `anyname.json`) in the same folder as `main.py`.
  - The code expects only **one** `.json` file to be present in that folder.

## 🧪 Status

The project is considered **complete** for now. Contributions are welcome, but active development is not currently planned.

## 📄 License

This project is licensed under the [MIT License](LICENSE).