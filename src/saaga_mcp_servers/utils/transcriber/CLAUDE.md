# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a speech-to-text transcription service implemented as an MCP (Model Context Protocol) server using AssemblyAI. It transcribes audio and video files into structured JSON transcripts with word-level timing information.

## Architecture

### Core Components
- **MCP Server** (`__main__.py`): FastMCP server exposing `transcribe_file` and `read_transcript` tools
- **Service Layer** (`service/assemblyai.py`): AssemblyAI SDK wrapper with API key management
- **Transcription Logic** (`lib/transcribe.py`): Core transcription workflow implementation
- **Models** (`models/transcript.py`): Pydantic models for Word and Transcript with timing data
- **Utilities** (`utils/file_utils.py`): File validation for supported formats

### Supported Formats
Audio: MP3, WAV, M4A, FLAC, OGG
Video: MP4, WebM

### Supported Languages
11 languages: en, es, fr, de, it, pt, nl, hi, ja, zh, fi

## Development Commands

### Running the MCP Server
```bash
# Start the transcriber MCP server
python -m transcriber
```

### CLI Usage (via Fire)
```bash
# Transcribe a single file
python transcribe_file.py /path/to/audio.mp3 --language_code=en

# The transcript will be saved as transcript.json in the same directory
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest src/transcriber/tests/test_assemblyai.py

# Run with coverage
pytest --cov=transcriber --cov-report=term-missing
```

## Environment Configuration

Create a `.env` file at the project root:
```
ASSEMBLYAI_API_KEY=your_api_key_here
ASSEMBLYAI_API_KEY_2=backup_api_key  # Optional secondary key
```

## Key Implementation Details

### Parallel Processing
- Batch file processing uses `asyncio.gather()` for concurrent transcriptions
- Partial failures don't stop the entire batch - each file is processed independently

### Output Structure
Transcripts are saved as `transcript.json` with:
- `text`: Full transcribed text
- `words`: Array of word objects with:
  - `text`: The word
  - `start`: Start time in milliseconds
  - `end`: End time in milliseconds
  - `confidence`: Confidence score (0-1)
  - `speaker`: Speaker label (if available)

### Error Handling
- File validation occurs before API calls to prevent unnecessary charges
- API failures are caught and reported per-file in batch operations
- Missing API keys raise RuntimeError with clear messages

## Testing Patterns

Tests use mocking extensively:
- Mock AssemblyAI API responses for unit tests
- Mock file validation to test edge cases
- Parametrized tests cover all supported languages
- Fixtures in `conftest.py` handle path setup

## MCP Integration

The server runs on stdio transport and exposes:
- `transcribe_file`: Process single files or directories (with recursive option)
- `read_transcript`: Load previously saved transcript JSON files

Response format includes status ("success", "failure", "partial_success") and detailed results for each processed file.