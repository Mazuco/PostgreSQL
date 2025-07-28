# gen-embed.py
from sentence_transformers import SentenceTransformer
import psycopg2
import numpy as np

# Connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Load the model (it will download the first time)
model = SentenceTransformer("intfloat/e5-large-v2")  # Embedding com 1024 dimensões

# Important e5 tip: always prefix with "passage: " or "query: "
def prepare_text(text):
    return "passage: " + text.strip()

# Search for documents not yet embedded
cur.execute("""
    SELECT d.id, d.content
      FROM documents d
     LEFT JOIN document_embeddings e ON d.id = e.id
     WHERE e.id IS NULL;
""")

rows = cur.fetchall()

for doc_id, content in rows:
    content_prepared = prepare_text(content)
    embedding = model.encode(content_prepared).tolist()

    if len(embedding) != 1024:
        print(f"[ERRO] Embedding of unexpected size: {len(embedding)}")
        continue

    # Insert into the bank
    cur.execute(
        "INSERT INTO document_embeddings (id, embedding) VALUES (%s, %s)",
        (doc_id, embedding)
    )
    print(f"✅ Inserted ID {doc_id}")

conn.commit()
cur.close()
conn.close()
