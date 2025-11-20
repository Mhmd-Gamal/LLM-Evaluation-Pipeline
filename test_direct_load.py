#!/usr/bin/env python
"""Direct test of model loading without device_map."""
import torch
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

model_name = "microsoft/Phi-3-mini-4k-instruct"
cache_dir = "./models"

logger.info("Step 1: Load tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, trust_remote_code=True)
logger.info("Tokenizer loaded OK")

logger.info("Step 2: Load model without device_map (straight to CPU)...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir=cache_dir,
    torch_dtype=torch.float32,
    trust_remote_code=True,
    attn_implementation="eager"
)
logger.info("Step 2 OK - model loaded from disk")

logger.info("Step 3: Move model to CPU...")
model = model.cpu()
logger.info("Step 3 OK - model on CPU")

logger.info("Step 4: Quick test...")
inputs = tokenizer("What is AI?", return_tensors="pt")
with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=5)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
logger.info(f"Response: {response}")
logger.info("SUCCESS!")
