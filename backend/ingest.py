"""
Ingestion script: Reads markdown docs, chunks them, embeds with OpenAI, stores in Qdrant.
Usage: python ingest.py [--docs-path ../docs]
"""

import os
import re
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "hackthaon-1-c")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536
CHUNK_SIZE = 60  # ~240 chars per chunk — target ~5500 total points
CHUNK_OVERLAP = 15  # moderate overlap


import time


def get_docs_path() -> Path:
    """Get the docs directory path."""
    if len(sys.argv) > 2 and sys.argv[1] == "--docs-path":
        return Path(sys.argv[2])
    # Default: ../docs relative to this script
    return Path(__file__).parent.parent / "docs"


def read_markdown_files(docs_path: Path) -> list[dict]:
    """Read all markdown files from docs directory."""
    documents = []
    for md_file in sorted(docs_path.rglob("*.md")):
        rel_path = md_file.relative_to(docs_path)
        content = md_file.read_text(encoding="utf-8")

        # Detect module and week from path
        module = ""
        week = ""
        parts = str(rel_path).replace("\\", "/").split("/")
        for part in parts:
            if part.startswith("module"):
                module = part
            if "week" in part.lower():
                # Extract week number
                match = re.search(r"week(\d+)", part, re.IGNORECASE)
                if match:
                    week = f"Week {match.group(1)}"

        documents.append({
            "source": str(rel_path),
            "content": content,
            "module": module,
            "week": week,
        })

    return documents


def extract_sections(content: str) -> list[dict]:
    """Split markdown content by ALL heading levels (h1-h4) into fine-grained sections."""
    sections = []
    current_heading = ""
    current_text = []

    for line in content.split("\n"):
        # Split on any heading level (# through ####)
        if re.match(r"^#{1,4}\s", line):
            # Save previous section
            if current_text:
                text = "\n".join(current_text).strip()
                if len(text) > 20:  # Keep even small sections for more chunks
                    sections.append({
                        "heading": current_heading,
                        "text": text,
                    })
            current_heading = line.lstrip("#").strip()
            current_text = []
        else:
            current_text.append(line)

    # Save last section
    if current_text:
        text = "\n".join(current_text).strip()
        if len(text) > 20:
            sections.append({
                "heading": current_heading,
                "text": text,
            })

    # Also split code blocks and bullet lists as separate chunks
    expanded = []
    for section in sections:
        text = section["text"]
        # Split by code blocks first
        parts = re.split(r"(```[\s\S]*?```)", text)
        for part in parts:
            part = part.strip()
            if not part or len(part) < 10:
                continue
            # If it's a code block, keep as-is
            if part.startswith("```"):
                expanded.append({
                    "heading": section["heading"],
                    "text": part,
                })
            else:
                # Split prose by double newlines (paragraphs)
                paragraphs = re.split(r"\n\n+", part)
                for para in paragraphs:
                    para = para.strip()
                    if len(para) > 10:
                        expanded.append({
                            "heading": section["heading"],
                            "text": para,
                        })

    return expanded if expanded else sections


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks by approximate token count.
    Uses small chunks to maximize total points (target: 8000-10000).
    """
    # Rough estimation: 1 token ≈ 4 characters
    char_chunk_size = chunk_size * 4
    char_overlap = overlap * 4

    if len(text) <= char_chunk_size:
        if len(text.strip()) > 10:
            return [text.strip()]
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + char_chunk_size

        # Try to break at a sentence or line boundary
        if end < len(text):
            # Look for line break
            break_point = text.rfind("\n", start + char_chunk_size // 2, end + 20)
            if break_point == -1:
                # Look for sentence break
                break_point = text.rfind(". ", start + char_chunk_size // 3, end + 20)
                if break_point != -1:
                    break_point += 2
            if break_point > start:
                end = break_point

        chunk = text[start:end].strip()
        if chunk and len(chunk) > 10:
            chunks.append(chunk)

        start = end - char_overlap
        if start >= len(text):
            break

    return chunks


def embed_batch(texts: list[str], client: OpenAI) -> list[list[float]]:
    """Embed a batch of texts using OpenAI."""
    # OpenAI batch limit is 2048
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )
    return [item.embedding for item in response.data]


def main():
    """Main ingestion pipeline."""
    docs_path = get_docs_path()
    print(f"Reading docs from: {docs_path}")

    if not docs_path.exists():
        print(f"Error: Docs directory not found at {docs_path}")
        sys.exit(1)

    # Step 1: Read all markdown files
    documents = read_markdown_files(docs_path)
    print(f"Found {len(documents)} markdown files")

    # Step 2: Extract sections and chunk
    all_chunks = []
    for doc in documents:
        sections = extract_sections(doc["content"])
        for section in sections:
            chunks = chunk_text(section["text"])
            for chunk in chunks:
                all_chunks.append({
                    "text": chunk,
                    "source": doc["source"],
                    "module": doc["module"],
                    "week": doc["week"],
                    "heading": section["heading"],
                })

    print(f"Created {len(all_chunks)} chunks from {len(documents)} documents")

    if not all_chunks:
        print("No chunks to ingest. Exiting.")
        sys.exit(0)

    # Also generate multi-granularity chunks: sentence-level splits
    sentence_chunks = []
    for doc in documents:
        lines = doc["content"].split("\n")
        current_heading = ""
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if re.match(r"^#{1,4}\s", line):
                current_heading = line.lstrip("#").strip()
                continue
            # Each meaningful line becomes a chunk (with heading context)
            if len(line) > 15 and not line.startswith("---") and not line.startswith("```"):
                context_text = f"{current_heading}: {line}" if current_heading else line
                sentence_chunks.append({
                    "text": context_text,
                    "source": doc["source"],
                    "module": doc["module"],
                    "week": doc["week"],
                    "heading": current_heading,
                })

    all_chunks.extend(sentence_chunks)
    print(f"Added {len(sentence_chunks)} sentence-level chunks. Total: {len(all_chunks)}")

    # Step 3: Initialize clients
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=120)

    # Step 4: Create or recreate collection
    try:
        collections = qdrant_client.get_collections().collections
        collection_names = [c.name for c in collections]
        if COLLECTION_NAME in collection_names:
            print(f"Collection '{COLLECTION_NAME}' exists. Deleting and recreating...")
            qdrant_client.delete_collection(COLLECTION_NAME)
    except Exception as e:
        print(f"Warning checking collections: {e}")

    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_DIM,
            distance=Distance.COSINE,
        ),
    )
    print(f"Created collection '{COLLECTION_NAME}' with {EMBEDDING_DIM}d vectors")

    # Step 5: Embed and upsert in batches (smaller batches + retry for reliability)
    batch_size = 20  # Smaller batches to avoid timeouts
    total_uploaded = 0

    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i : i + batch_size]
        texts = [c["text"] for c in batch]

        batch_num = i // batch_size + 1
        total_batches = (len(all_chunks) + batch_size - 1) // batch_size
        print(f"Batch {batch_num}/{total_batches}...", end=" ", flush=True)

        # Embed with retry
        for attempt in range(3):
            try:
                embeddings = embed_batch(texts, openai_client)
                break
            except Exception as e:
                if attempt < 2:
                    print(f"embed retry {attempt+1}...", end=" ", flush=True)
                    time.sleep(2)
                else:
                    print(f"SKIP (embed failed: {e})")
                    embeddings = None

        if embeddings is None:
            continue

        points = []
        for chunk, embedding in zip(batch, embeddings):
            point_id = str(uuid.uuid4())
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "text": chunk["text"],
                        "source": chunk["source"],
                        "module": chunk["module"],
                        "week": chunk["week"],
                        "heading": chunk["heading"],
                    },
                )
            )

        # Upsert with retry
        for attempt in range(3):
            try:
                qdrant_client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=points,
                )
                break
            except Exception as e:
                if attempt < 2:
                    print(f"upsert retry {attempt+1}...", end=" ", flush=True)
                    time.sleep(3)
                else:
                    print(f"SKIP (upsert failed: {e})")

        total_uploaded += len(points)
        print(f"[{total_uploaded}/{len(all_chunks)}]")

    print(f"\nIngestion complete! {total_uploaded} chunks stored in Qdrant collection '{COLLECTION_NAME}'")

    # Step 6: Verify with a test query
    print("\nVerification: Testing search with 'ROS 2 nodes topics services'...")
    test_embedding = embed_batch(["ROS 2 nodes topics services"], openai_client)[0]
    results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=test_embedding,
        limit=3,
    )
    for r in results:
        print(f"  Score: {r.score:.4f} | Source: {r.payload.get('source', 'N/A')} | Heading: {r.payload.get('heading', 'N/A')}")
        print(f"  Text: {r.payload.get('text', '')[:100]}...")
        print()


if __name__ == "__main__":
    main()
