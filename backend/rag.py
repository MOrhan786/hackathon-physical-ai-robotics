import os
from openai import OpenAI
from qdrant_client import QdrantClient


QDRANT_URL = os.getenv("QDRANT_URL", "")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "hackthaon-1-c")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"


def get_qdrant_client() -> QdrantClient:
    """Get Qdrant client instance."""
    return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


def get_openai_client() -> OpenAI:
    """Get OpenAI client instance."""
    return OpenAI(api_key=OPENAI_API_KEY)


def embed_text(text: str) -> list[float]:
    """Generate embedding for a text using OpenAI."""
    client = get_openai_client()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def search_similar_chunks(query: str, top_k: int = 5) -> list[dict]:
    """Search Qdrant for similar text chunks."""
    qdrant = get_qdrant_client()
    query_embedding = embed_text(query)

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k,
        with_payload=True,
    )

    chunks = []
    for result in results:
        payload = result.payload or {}
        chunks.append({
            "text": payload.get("text", ""),
            "source": payload.get("source", ""),
            "heading": payload.get("heading", ""),
            "module": payload.get("module", ""),
            "week": payload.get("week", ""),
            "score": result.score,
        })

    return chunks


def build_chat_prompt(
    query: str,
    chunks: list[dict],
    history: list[dict] | None = None,
    selected_text: str | None = None,
) -> list[dict]:
    """Build the chat prompt with RAG context."""

    # System message
    system_message = """You are an expert AI teaching assistant for the "Physical AI & Humanoid Robotics" textbook.
Your role is to help students understand concepts from the course covering:
- Module 1: ROS 2 Fundamentals (Weeks 1-5)
- Module 2: Gazebo & Unity Simulation (Weeks 6-7)
- Module 3: NVIDIA Isaac Platform (Weeks 8-10)
- Module 4: Humanoid Development & Conversational Robotics (Weeks 11-13)

Guidelines:
- Answer ONLY based on the provided textbook context. If the answer isn't in the context, say so.
- Use clear, educational language appropriate for students.
- Include code examples when relevant.
- Reference specific weeks/modules when applicable.
- Format responses in markdown for readability.
- If asked to navigate, suggest the relevant section with [[REDIRECT:/docs/path#heading]] format."""

    # Build context from retrieved chunks
    context_parts = []
    for chunk in chunks:
        source_info = ""
        if chunk.get("module"):
            source_info += f"Module: {chunk['module']}"
        if chunk.get("week"):
            source_info += f" | Week: {chunk['week']}"
        if chunk.get("heading"):
            source_info += f" | Section: {chunk['heading']}"

        context_parts.append(f"[Source: {source_info}]\n{chunk['text']}")

    context_text = "\n\n---\n\n".join(context_parts)

    # Build messages
    messages = [{"role": "system", "content": system_message}]

    # Add context
    context_msg = f"## Relevant Textbook Content:\n\n{context_text}"
    if selected_text:
        context_msg += f"\n\n## User's Selected Text (from page):\n{selected_text}"

    messages.append({"role": "system", "content": context_msg})

    # Add history
    if history:
        for h in history[-6:]:  # Last 6 exchanges max
            if h.get("user_message"):
                messages.append({"role": "user", "content": h["user_message"]})
            if h.get("ai_response"):
                messages.append({"role": "assistant", "content": h["ai_response"]})

    # Add current query
    messages.append({"role": "user", "content": query})

    return messages


def chat(
    message: str,
    history: list[dict] | None = None,
    selected_text: str | None = None,
) -> str:
    """Process a chat message with RAG pipeline."""

    # Step 1: Search for relevant chunks
    search_query = message
    if selected_text:
        search_query = f"{message} {selected_text[:200]}"

    chunks = search_similar_chunks(search_query, top_k=5)

    # Step 2: Build prompt with context
    messages = build_chat_prompt(message, chunks, history, selected_text)

    # Step 3: Get completion from OpenAI
    client = get_openai_client()
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=2000,
    )

    return response.choices[0].message.content or "I couldn't generate a response."


def personalize_content(content: str, user_background: dict) -> str:
    """Personalize chapter content based on user background."""
    client = get_openai_client()

    prog_exp = user_background.get("programming_experience", "intermediate")
    robo_exp = user_background.get("robotics_experience", "none")
    languages = user_background.get("preferred_languages", ["Python"])
    hardware = user_background.get("hardware_access", [])

    prompt = f"""You are an expert educator. Rewrite the following textbook content to be personalized for a student with this background:

- Programming Experience: {prog_exp}
- Robotics Experience: {robo_exp}
- Preferred Languages: {', '.join(languages)}
- Hardware Access: {', '.join(hardware) if hardware else 'None'}

Adaptation rules:
- For BEGINNERS: Add more explanations, analogies, step-by-step breakdowns. Simplify jargon.
- For INTERMEDIATE: Keep the current depth but add practical tips and common pitfalls.
- For ADVANCED: Add advanced concepts, optimization techniques, research references.
- Tailor code examples to their preferred programming language when possible.
- If they have specific hardware, mention how concepts apply to that hardware.
- Preserve ALL code blocks and technical accuracy.
- Keep the same structure (headings, sections) but adapt the explanations.
- Output in markdown format.

Content to personalize:
{content[:8000]}"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=4000,
    )

    return response.choices[0].message.content or content


def translate_content(content: str, target_language: str) -> str:
    """Translate chapter content to target language."""
    client = get_openai_client()

    prompt = f"""You are an expert translator. Translate the following technical textbook content to {target_language}.

Translation rules:
- Keep ALL code blocks, variable names, function names, and technical commands in English.
- Translate explanations, descriptions, and prose to {target_language}.
- Maintain the same markdown structure (headings, bullet points, code blocks).
- Keep proper nouns (ROS 2, NVIDIA Isaac, Gazebo, Python, etc.) in English.
- Ensure technical accuracy is preserved.
- Output in markdown format.

Content to translate:
{content[:8000]}"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=4000,
    )

    return response.choices[0].message.content or content
