# Gemma 4 E2B Validation Setup - Ollama/LM Studio

## Option 1: Using Ollama (Recommended)

### Installation
1. **Download & Install Ollama**
   - macOS: Download from https://ollama.ai
   - Linux: `curl https://ollama.ai/install.sh | sh`
   - Windows: Download from https://ollama.ai

2. **Pull Gemma Model**
   ```bash
   ollama pull gemma:7b
   # or for gemma2
   ollama pull gemma2:9b
   ```

3. **Start Ollama Server**
   ```bash
   ollama serve
   ```
   The server will run on `http://localhost:11434`

### Verify Installation
```bash
curl http://localhost:11434/api/tags
```

---

## Option 2: Using LM Studio

### Installation
1. **Download & Install LM Studio**
   - Visit: https://lmstudio.ai/
   - Download for macOS/Windows/Linux

2. **Download Gemma Model**
   - Open LM Studio
   - Search for "gemma-4-e2b" or "gemma2" in the Model Hub
   - Click "Download"

3. **Start Local Server**
   - Go to "Local Server" tab
   - Select your downloaded model from dropdown
   - Configure:
     - Context length: 8192
     - GPU layers: Maximum (or 20+ for good performance)
     - Port: 1234 (default)
   - Click "Start Server"

### Verify Installation
```bash
curl http://localhost:1234/v1/models
```

---

## Configuration

Create a `.env` file in the project root:

```env
# For Ollama (default)
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=gemma:7b

# OR For LM Studio
# LLM_PROVIDER=lm_studio
# LLM_BASE_URL=http://localhost:1234
# LLM_MODEL=gemma-4-e2b-it

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Performance Tips

### For Ollama:
- Increase context length: `ollama run gemma:7b --num-ctx 8192`
- GPU acceleration (automatic on supported systems)

### For LM Studio:
- Adjust GPU layers based on your VRAM:
  - 8GB GPU: 15-20 layers
  - 12GB+ GPU: 30+ layers
- Use smaller models for faster inference (gemma:7b is recommended)

---

## Running Both Together (Optional)

If you want to compare models, run both on different ports:

```bash
# Terminal 1: Ollama on 11434
ollama serve

# Terminal 2: LM Studio on 1234
# (Configure in LM Studio GUI)
```

Then update `.env` to test one at a time, or modify the API to support both.
