# Retrieval-Augmented Generation (RAG) Chatbot for Customer Support

## Description

This project implements a Retrieval-Augmented Generation (RAG) chatbot designed specifically to assist users by answering queries related to customer support. It leverages customer support documentation from Angel One (https://www.angelone.in/support) and provided insurance PDF documents as its knowledge base. The chatbot only answers queries based on these provided sources and clearly indicates when a question falls outside of its domain knowledge.

## Features

- **RAG Implementation:** Utilizes Retrieval-Augmented Generation methodology for accurate responses.
- **Document Scraping:** Automated scraping of Angel One support pages.
- **PDF Processing:** Processes PDF documents to incorporate their content into the chatbot's knowledge base.
- **Interactive Interface:** User-friendly interface powered by Streamlit for seamless interaction.
- **Clear Response Handling:** Responds with `I Don't know` when asked out-of-scope questions.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- wkhtmltopdf (for PDF generation)

## Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/aarishmkhan/RAG_Chatbot
cd RAG_Chatbot
```

2. **Install Python Dependencies:**

```bash
pip install -r requirements.txt
```

3. **Install wkhtmltopdf:**
- Download and install from [wkhtmltopdf downloads](https://wkhtmltopdf.org/downloads.html).
- Ensure it is added to your system PATH.

4. **Environment Variables:**
- Create a `.env` file in the root directory and add your HuggingFace API token:

```bash
HUGGINGFACE_API_TOKEN=your_huggingface_api_token_here
```

## Data Preparation

- Run `scrape.py` to scrape the Angel One support pages and generate a consolidated PDF:

```bash
python scrape.py
```

- Ensure insurance-related PDFs are placed in the project root directory.

## Usage

### Starting the Chatbot

Run the Streamlit app:

```bash
streamlit run streamlit.py
```

Open your browser and navigate to:

```
http://localhost:8501
```

### Interacting with the Chatbot

- Input your queries in the chat interface.
- The bot responds with relevant information from the provided sources or explicitly states 'I don't know' if the query is beyond the knowledge base.

## Project Structure

```bash
.
├── main.py
├── scrape.py
├── streamlit.py
├── requirements.txt
├── angelone_support_pages.pdf
├── *.pdf (insurance PDFs)
└── README.md
```

## Dependencies

- Streamlit
- LangChain
- HuggingFace
- FAISS
- pdfkit
- BeautifulSoup
- Requests

(Refer to `requirements.txt` for exact package versions.)

Ensure necessary environment variables and dependencies are configured on the hosting platform.

