from transformers import pipeline

def summarize_text(text, max_length=100, min_length=10):
    summarization = pipeline("summarization")
    result = summarization(text, max_length=max_length, min_length=min_length, do_sample=False)
    summarized_text = result[0]['summary_text']
    return summarized_text