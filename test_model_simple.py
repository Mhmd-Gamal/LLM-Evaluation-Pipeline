#!/usr/bin/env python
"""Simple test to debug model loading."""
import torch
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    model_name = "microsoft/Phi-3-mini-4k-instruct"
    cache_dir = "./models"
    
    logger.info(f"Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        cache_dir=cache_dir,
        trust_remote_code=True
    )
    logger.info("Tokenizer loaded successfully")
    
    logger.info(f"Loading model on CPU with float32...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        cache_dir=cache_dir,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        attn_implementation="eager"
    )
    logger.info("Model loaded successfully, moving to CPU...")
    model = model.to("cpu")
    logger.info("Model successfully moved to CPU")
    
    logger.info("Testing inference...")
    inputs = tokenizer("What is AI?", return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=10)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    logger.info(f"Response: {response}")
    
    logger.info("SUCCESS: Model works!")
    
except Exception as e:
    logger.error(f"ERROR: {e}", exc_info=True)
