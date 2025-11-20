# Pidima LLM Evaluation Project - Setup Complete

## Project Status: READY TO RUN

The Pidima LLM Evaluation Pipeline project has been successfully set up and is ready for execution.

###Installed Components:
- ✓ Virtual environment created (`venv`)
- ✓ All Python dependencies installed (FastAPI, PyTorch, Transformers, etc.)
- ✓ Model cache directory prepared (`./models`)
- ✓ Project structure verified

### How to Run the Project

#### Option 1: Local Python Server (Current Setup)
```bash
# Activate virtual environment (if not already active)
.\venv\Scripts\Activate.ps1

# Start the FastAPI server
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000

# In another terminal, run the evaluation (use -m flag to properly import modules)
python -m src.evaluation.run_evaluation
```

#### Option 2: Docker Compose (Recommended for Prod)
```bash
# Start all services
docker-compose up --build

# In another terminal, run evaluation
docker exec -it pidima-llm-api python src/evaluation/run_evaluation.py
```

### API Endpoints (Once Server Starts)

1. **Health Check** - `GET /health`
   ```bash
   curl http://localhost:8000/health
   ```

2. **Generate Text** - `POST /generate`
   ```bash
   curl -X POST http://localhost:8000/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt": "What is AI?", "max_tokens": 100}'
   ```

3. **Evaluate MCQ** - `POST /evaluate_mcq`
   ```bash
   curl -X POST http://localhost:8000/evaluate_mcq \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is the capital of France?",
       "options": ["London", "Berlin", "Paris", "Madrid"]
     }'
   ```

4. **Interactive API Docs** - Visit `http://localhost:8000/docs`

### Project Architecture

- **Model**: microsoft/Phi-3-mini-4k-instruct (3.8B parameters)
- **Framework**: FastAPI + Transformers + PyTorch
- **Dataset**: MMLU (Massive Multitask Language Understanding)
- **Evaluation**: 150 questions across 10 categories

### Running Evaluation

Once the API server is running, in a separate terminal:
```bash
python -m src.evaluation.run_evaluation
```

This will:
1. Download MMLU dataset from HuggingFace
2. Evaluate 150 questions through the API
3. Generate comprehensive metrics and visualizations
4. Create error analysis report in `./results/`

### Expected Performance

- **Model Loading**: 10-20 minutes on first startup (CPU only)
- **Overall Accuracy**: 65-75% (on MMLU benchmark)
- **Response Time**: 500-1000ms per question (CPU inference)
- **Total Evaluation Time**: ~30-50 minutes for 150 questions
- **Memory Usage**: 4-6 GB during inference
- **Disk Space**: ~20GB for model cache

### Project Files

Key source files:
- `src/api/main.py` - FastAPI application with 3 endpoints
- `src/llm/loader.py` - Model loading and optimization
- `src/llm/inference.py` - Inference engine for text generation
- `src/evaluation/run_evaluation.py` - Evaluation pipeline
- `src/evaluation/metrics.py` - Metrics calculation

### Configuration

The project uses environment variables for configuration. Create a `.env` file from the template:
```bash
cp env.sh .env
```

Key settings:
- `MODEL_NAME`: HuggingFace model identifier
- `DEVICE`: cpu or cuda
- `EVAL_BATCH_SIZE`: Number of concurrent requests (default: 5)
- `LOG_LEVEL`: INFO, DEBUG, etc.

### Troubleshooting

**Model Loading Takes a Long Time:**
- The 3.8B Phi-3 model requires significant CPU resources
- **First startup: 10-20 minutes** is normal while PyTorch initializes the model
- **Subsequent runs**: Much faster due to caching
- Do NOT interrupt the process - let it complete
- Monitor system resources but do not close the terminal

**If the server appears stuck:**
1. Check that you see the message "Loading model..." in the logs
2. Wait at least 15 minutes before concluding it's hung
3. Check available disk space (need ~20GB free)
4. Ensure no other heavy processes are running
5. If truly stuck after 20 minutes, restart with fewer background applications running

**Memory issues:**
- Ensure 8GB+ RAM available
- Close other applications (browsers, editors, etc.)
- Reduce `EVAL_BATCH_SIZE` in .env if needed

**API not responding:**
- Wait for "Model loaded successfully!" message
- Check that you see "Application startup complete"
- Then test the health endpoint

### Next Steps

1. **Start the API server:**
   ```bash
   .\venv\Scripts\Activate.ps1
   python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
   ```

2. **Wait for startup** - You should see these messages in order:
   ```
   INFO: Started server process
   INFO: Waiting for application startup
   Loading model...
   Loading checkpoint shards: 100%|████████| 2/2
   Model loaded successfully!
   Application startup complete
   Uvicorn running on http://127.0.0.1:8000
   ```

3. **Once server is ready** (you see "Application startup complete"), open a new terminal and test:
   ```bash
   curl http://localhost:8000/health
   ```

4. **Run evaluation** in another terminal:
   ```bash
   python -m src.evaluation.run_evaluation
   ```

5. **Check results** in the `./results/` directory

---

**Project**: Pidima AI Engineer Challenge - LLM Evaluation Pipeline
**Candidate**: Mohamed Gamal Elbayoumi
