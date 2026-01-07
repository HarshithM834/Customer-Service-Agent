# AI Customer Support Agent

A multimodal AI agent designed for enterprise customer support, capable of handling billing, sales, and technical support inquiries via text and voice.

## Features

*   **Multi-Agent Routing**: Intelligently routes queries to specialized agents (Billing, Sales, Tech Support).
*   **Multimodal Interaction**: Supports both text chat and voice interactions (powered by ElevenLabs).
*   **Context Retrieval**: Uses Perplexity AI to fetch real-time, accurate information.
*   **Intent Classification**: Powered by Gemini 2.0 Flash for fast and accurate intent detection.

## Prerequisites

*   Python 3.10+
*   API Keys:
    *   Google Gemini API
    *   Perplexity API (Optional, for context)
    *   ElevenLabs API (Optional, for voice)

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ai-customer-support-agent.git
    cd ai-customer-support-agent
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Configure environment variables:
    Create a `.env` file in the root directory:
    ```env
    GEMINI_API_KEY=your_gemini_key
    PERPLEXITY_API_KEY=your_perplexity_key
    ELEVENLABS_API_KEY=your_elevenlabs_key
    ```

## Usage

### Run the Demo
Test the agent's capabilities with pre-defined scenarios:
```bash
python3 demo.py
```

### Start the API Server
Run the FastAPI backend:
```bash
python3 main.py
```
 The server will start at `http://0.0.0.0:8000`.

## License

[MIT](LICENSE)
