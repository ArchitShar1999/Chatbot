from llama_cpp import Llama
import os

MODEL_PATH = "./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=512,                 # 🔥 small context = FAST
    n_threads=os.cpu_count(),   # use all CPU cores
    n_batch=512,               # big batch = FAST
    n_gpu_layers=0,             # CPU only (safe)
    f16_kv=True,
    use_mmap=True,
    verbose=False
)
