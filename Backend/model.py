from llama_cpp import Llama
import os

MODEL_PATH = "./models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,                 # 🔥 small context = FAST
    n_threads=os.cpu_count(),   # use all CPU cores
    n_batch=1024,               # big batch = FAST
    n_gpu_layers=0,             # CPU only (safe)
    f16_kv=True,
    use_mmap=True,
    verbose=False
)
