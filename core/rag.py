import os
import requests
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

load_dotenv()
COLLECTION = "notes"


def _headers():
    return {"Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"}


def embed(texts: list[str], task: str) -> list[list[float]]:
    """Turn text into numbers. task = 'retrieval.passage' (notes) or 'retrieval.query' (questions)."""
    r = requests.post(
        "https://api.jina.ai/v1/embeddings",
        headers=_headers(),
        json={"model": "jina-embeddings-v3", "task": task, "input": texts},
        timeout=60,
    )
    r.raise_for_status()
    return [d["embedding"] for d in r.json()["data"]]


def rerank(query: str, docs: list[str], top_n: int = 3) -> list[str]:
    """Re-sort chunks so the most relevant come first."""
    r = requests.post(
        "https://api.jina.ai/v1/rerank",
        headers=_headers(),
        json={
            "model": "jina-reranker-v2-base-multilingual",
            "query": query,
            "documents": docs,
            "top_n": top_n,
        },
        timeout=60,
    )
    r.raise_for_status()
    return [docs[item["index"]] for item in r.json()["results"]]


def build_index(folder: str = "knowledge"):
    """Read notes, chunk them, embed them, store them in Qdrant."""
    if not os.path.isdir(folder) or not os.listdir(folder) or not os.getenv("JINA_API_KEY"):
        return None  # no notes or no key: the app still works without RAG

    docs = SimpleDirectoryReader(folder).load_data()
    nodes = SentenceSplitter(chunk_size=512, chunk_overlap=50).get_nodes_from_documents(docs)
    texts = [n.get_content() for n in nodes]
    vectors = embed(texts, "retrieval.passage")

    client = QdrantClient(":memory:")  # lives in RAM, rebuilt each launch
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE),
    )
    client.upsert(
        collection_name=COLLECTION,
        points=[
            PointStruct(id=i, vector=v, payload={"text": t})
            for i, (t, v) in enumerate(zip(texts, vectors))
        ],
    )
    return client


def retrieve(client, query: str) -> str:
    """Find the notes most relevant to a question."""
    if client is None:
        return ""
    qvec = embed([query], "retrieval.query")[0]
    hits = client.query_points(collection_name=COLLECTION, query=qvec, limit=8).points
    chunks = [h.payload["text"] for h in hits]
    if not chunks:
        return ""
    return "\n---\n".join(rerank(query, chunks, top_n=3))