# Vox Agent OS

A voice-first agent interface that lets you interact with AI tools using natural language.

## 🎯 Current Features (MVP)

- 🎤 **Voice Commands**: Record voice input with a simple CLI interface
- 🔄 **Transcription**: Convert speech to text using OpenAI's Whisper API
- 📝 **Text Summarization**: Summarize text using GPT-4
- 🔊 **Voice Response**: Hear responses through text-to-speech (using macOS `say` command)

## 🚀 Getting Started

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

3. **Example command**:
   Say: "Summarize this text: AgentOS is a platform for creating AI agents"

## 📦 Project Structure
vox-agent-os/
├── packages/
│ └── vox/
│ ├── kernel/ # Core agent logic
│ ├── voice/ # Voice recording and TTS
│ ├── tools/ # Tool implementations
│ └── interfaces/ # CLI interface
├── examples/ # Usage examples
└── docs/ # Documentation

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

## 📜 License

MIT License - see LICENSE file for details
