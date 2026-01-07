# Sales AI Agent

A sophisticated multi-agent sales assistant powered by **Google Gemini**, **Perplexity AI**, and **ElevenLabs**. This agent specializes in handling sales inquiries, including new plan subscriptions, device recommendations, upgrades, and improved customer acquisition.

## 🚀 Key Features

*   **Multi-Agent Architecture**: Intelligent routing system that directs queries to specialized agents:
    *   **New Customer Agent**: Focuses on acquisition, onboarding, and plan explanation for new users.
    *   **Upgrade Agent**: Handles existing customer upgrades and retention offers.
    *   **Device Agent**: Expert on smartphones, tablets, and accessories.
    *   **Promotion Agent**: Details current deals and bundles.
*   **Intelligent Intent Classification**: Uses Gemini (Flash 2.0) to accurately determine customer intent.
*   **Real-time Context**: Integrates with **Perplexity AI** to fetch up-to-date device specs and plan comparisons.
*   **Voice Capability**: Generates natural-sounding voice responses using **ElevenLabs**.
*   **FastAPI Backend**: Robust, asynchronous API serving chat and voice endpoints.

## 🛠️ Technology Stack

*   **Core LLM**: Google Gemini 2.0 Flash
*   **Context/Search**: Perplexity AI
*   **Text-to-Speech**: ElevenLabs
*   **Framework**: FastAPI / Uvicorn
*   **Language**: Python 3.10+

## 📋 Prerequisites

*   Python 3.9 or higher
*   API Keys for Gemini (Required), Perplexity (Optional), and ElevenLabs (Optional)

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/sales-agent.git
cd sales-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the root directory:
```env
# Required
GEMINI_API_KEY=your_gemini_key_here

# Optional (for enhanced features)
PERPLEXITY_API_KEY=your_perplexity_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
```

### 4. Run the Application
```bash
# Start the backend server
python main.py
```
The API will be available at `http://localhost:8002`.

## 🧪 Testing

The project includes a comprehensive test suite for sales scenarios.

```bash
# Run the sales verification demo
python demo.py
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Main text chat interface. Accepts `{"message": "..."}`. |
| POST | `/voice` | Voice-enabled chat. Returns text + audio data. |
| GET | `/logs` | Retrieve session interaction history. |
| GET | `/health` | Service health check. |

## 📂 Project Structure

```
├── agents.py             # Agent definitions (New Customer, Upgrade, Device) and Router
├── services.py           # LLM and API integration logic
├── main.py               # FastAPI application entry point
├── demo.py               # Verification and demo script
├── requirements.txt      # Project dependencies
└── .env                  # Configuration (not committed)
```
