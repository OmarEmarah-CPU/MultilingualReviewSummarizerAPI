# MultilingualReviewSummarizerAPI
REST API for multilingual customer review summarization with semantic keyword detection.

# Multilingual Review Summarizer API with Semantic Keyword Detection

This project implements a backend REST API that processes multilingual customer reviews (e.g., Arabic, Spanish) to generate concise English summaries and detect semantic keywords.

## Features

- **API & Authentication**
  - Client registration with API key issuance
  - Protected endpoints for review processing

- **Multilingual Handling**
  - Automatic language detection
  - Translation of reviews into English

- **Text Preprocessing**
  - Cleans and normalizes noisy, user-generated content
  - Handles mixed languages and irregular formatting

- **Summarization**
  - Produces a single, concise summary (max two sentences)
  - Captures overall sentiment and key themes

- **Semantic Keyword Detection**
  - Detects keywords based on meaning, not exact matches
  - Returns a structured JSON mapping of keywords to detected phrases
