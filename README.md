# Autonomous Research Direction Generation System

A multi-agent system for automated trend analysis and research innovation proposals.

## 📌 Project Overview

This system implements three specialized agents that collaboratively:
1. **Research Agent**: Continuously gathers tech-related data from external APIs
2. **Analysis Agent**: Identifies emerging trends using NLP and clustering
3. **Innovation Agent**: Generates prioritized research proposals with confidence scoring

## 🚀 Key Features

- **Real-time Data Processing**: API integration with fallback to simulated data
- **Technical Trend Detection**: Advanced TF-IDF vectorization with tech-specific lexicon
- **Adaptive Clustering**: Dynamic cluster sizing based on dataset characteristics
- **Innovation Pipeline**: Confidence-scored ideas with duplicate prevention
- **Thread-safe Messaging**: Custom message bus for inter-agent communication

## ⚙️ System Architecture

```plaintext
Data Flow:
Research Agent → Message Bus → Analysis Agent → Message Bus → Innovation Agent → Report

Components:
- ResearchAgent: Fetches/preprocesses data (newsapi.org implementation)
- AnalysisAgent: Performs trend detection (K-means clustering + TF-IDF)
- InnovationAgent: Generates research directions with impact scoring
- MessageBus: Thread-safe communication channel
