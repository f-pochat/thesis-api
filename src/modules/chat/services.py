import ollama

from src.logger import log
from src.modules.chat import repositories


def chat(history: list[dict], prompt: str, class_id: str) -> dict:
    summary, audio_text = repositories.get_processed_class(class_id)

    def call_ollama_with_context(history_msgs, query, summary_text, embed_context) -> dict:
        if context is None:
            messages = ([
                {"role": "system",
                 "content": system_prompt_no_context},
                {"role": "user", "content": f"{query}"}
            ])
        else:
            messages = ([
                            {"role": "system",
                             "content": system_prompt},
                            {"role": "user", "content": f"Contenido de la clase: {embed_context}"},
                            {"role": "user", "content": f"Resumen de la clase: {summary_text}"}] + history_msgs +
                        [{"role": "user", "content": f"{query}"}
                         ])
        response = ollama.chat(
            model="llama3.1",
            messages=messages
        )

        log.info(messages)

        return response['message']['content']

    context = find_most_relevant_context(query=prompt, class_id=class_id)

    return call_ollama_with_context(history, prompt, summary, context)


def find_most_relevant_context(query, class_id, model_name="tinyllama"):
    query_embedding = ollama.embeddings(model=model_name, prompt=query)
    most_relevant = repositories.get_most_relevant_embeddings(query_embedding["embedding"], class_id)
    return most_relevant


system_prompt = """
Eres Australito, un asistente virtual argentino diseñado para ayudar a estudiantes. Explica conceptos de forma clara, simple y adaptada al nivel del usuario. Si es relevante, usa el contenido de la clase proporcionado. Si no lo es, ignóralo. Siempre responde con un saludo amigable.
"""

system_prompt_no_context = """
Eres Australito, un asistente virtual argentino diseñado para ayudar a estudiantes. Siempre responde de forma amigable amigable.
"""
