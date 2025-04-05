# Vox Agent OS

A voice-first agent interface that lets you interact with AI tools using natural language.

## 🎯 Current Features (MVP)

- 🎤 **Voice Commands**: Record voice input with a simple CLI interface
- 🔄 **Transcription**: Convert speech to text using OpenAI's Whisper API
- 📝 **Text Summarization**: Summarize text using GPT-4
- 🔊 **Voice Response**: Hear responses through text-to-speech (using macOS `say` command)

## 🚀 Getting Started

This product supports only MacOS currently.

1. **Set up your environment**:
```bash
# Install dependencies
poetry install

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env
```

2. **Run the voice interface**:
```bash
poetry run vox speak
```
- Press Ctrl+C to stop recording
- Wait for the response

3. **Run the chat interface**:
```bash
poetry run vox chat
```

4. **Example command**:
   Say: "Summarize the PDF document about my tax receipts"
Note: The MVP only works currently if you use the words summarize and PDF in your command.

## 🛠️ Development

- Uses Poetry for dependency management
- OpenAI's Whisper API for speech-to-text
- GPT-4 for text summarization
- System TTS for voice output

## 🔜 Coming Soon

- Additional voice commands
- More AI tools
- Custom TTS options
- Continuous conversation mode

## 📦 Project Structure

```text
vox-agent-os/
├── LICENSE
├── README.md
├── docs
├── examples
├── logs
│   └── run.log
├── packages
│   └── vox
│       ├── agents
│       │   └── crew_ai
│       ├── interfaces
│       │   ├── android_proxy
│       │   ├── cli
│       │   └── desktop
│       ├── kernel
│       │   ├── __init__.py
│       │   └── agent.py
│       ├── memory
│       ├── tools
│       │   ├── pdf_reader.py
│       │   └── summarize.py
│       ├── utils
│       │   └── logging.py
│       └── voice
│           ├── recorder.py
│           ├── speaker.py
│           └── transcriber.py
├── poetry.lock
├── pyproject.toml
└── scripts
```

## 📜 License

MIT License - see LICENSE file for details
