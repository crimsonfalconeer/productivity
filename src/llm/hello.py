# src/llm/hello.py
import time, json, argparse, groq
from .config import API_KEY

MODELS = {
    "small":  "llama-3.1-8b-instant",
    "large":  "llama-3.3-70b-versatile",
}

def run(model: str, prompt: str):
    client = groq.Groq(api_key=API_KEY)
    tic = time.perf_counter()

    resp = client.chat.completions.create(
        model=MODELS[model],
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    toc = time.perf_counter()

    # ---- make the usage JSON-friendly ----
    usage = {
        "prompt_tokens":     resp.usage.prompt_tokens,
        "completion_tokens": resp.usage.completion_tokens,
        "total_tokens":      resp.usage.total_tokens,
    }

    print(json.dumps(
        {
            "model":      model,
            "latency_s":  round(toc - tic, 3),
            "tokens":     usage,
        },
        indent=2,
    ))
    print("\n--- assistant ---\n" + resp.choices[0].message.content)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model",  choices=["small", "large"], default="small")
    ap.add_argument("--prompt", default="Hello, world!")
    run(**vars(ap.parse_args()))
