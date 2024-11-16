import json

import ollama
from nltk import sent_tokenize

from src.modules.chat import repositories
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def chat(prompt: str, class_id: str) -> str:
    embeddings, audio_text = repositories.get_embeddings(class_id)
    audio_text = audio_text.tobytes().decode('utf-8')

    def call_ollama_with_context(query, embed_context) -> dict:
        response = ollama.generate(
            model="tinyllama",
            prompt=f"Contexto: {embed_context}\n\nPregunta: {query}"
        )

        return response

    sentences = split_audio_text(audio_text)

    context = find_most_relevant_context(query=prompt,
                                         embeddings=embeddings,
                                         texts=sentences)

    ollama_response = call_ollama_with_context(prompt, context)
    return ollama_response["response"]


def split_audio_text(audio_text: str) -> list:
    return sent_tokenize(audio_text)


def find_most_relevant_context(query, embeddings, texts, model_name="tinyllama", top_k=3):
    embeddings = json.loads(embeddings)
    embeddings = np.array(embeddings).reshape(1, -1)
    query_embedding = ollama.embeddings(model=model_name, prompt=query)
    query_embedding = np.array(query_embedding["embedding"]).reshape(1, -1)

    similarity_scores = cosine_similarity(query_embedding, embeddings).flatten()
    top_indices = np.argsort(similarity_scores)[-top_k:][::-1]

    return [texts[idx] for idx in top_indices]
