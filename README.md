# AI Tools GUI

A simple desktop application built with **CustomTkinter** that provides two AI-powered tools: **Sentiment Analysis** and **Sentence Similarity**. Both tools run locally via FastAPI servers and leverage **Hugging Face Inference API** for natural language processing.

## Features

- **Sentiment Analysis**
  - Analyze the sentiment of English text.
  - Outputs labels such as **POSITIVE**, **NEUTRAL**, or **NEGATIVE** with confidence scores.
  - Powered by `cardiffnlp/twitter-roberta-base-sentiment` model on Hugging Face.

- **Sentence Similarity**
  - Compare a source sentence with multiple other sentences.
  - Returns similarity scores between 0 and 1.
  - Uses `sentence-transformers/all-MiniLM-L6-v2` model for semantic similarity.

- **Desktop GUI**
  - Built with **CustomTkinter** for modern, responsive design.
  - Easy-to-use buttons to launch either tool.
  - Automatically starts both API servers in the background.
