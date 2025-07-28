#generate-embedOpenAI.py
import openai
import psycopg2
import os

# Configure API Key securely
client = openai.OpenAI(api_key="sk-....")  # replace with your key securely

# Embedding model
model_id = "text-embedding-ada-002"

# Connecting to PostgreSQL
conn = psycopg2.connect(database="postgres", user="postgres", host="localhost", port="5432")
cur = conn.cursor()

# Search for documents
cur.execute("SELECT id, content FROM documents")
documents = cur.fetchall()

# Generate and store embeddings
for doc_id, doc_content in documents:
    response = client.embeddings.create(input=doc_content, model=model_id)
    embedding = response.data[0].embedding
    cur.execute("INSERT INTO document_embeddings (id, embedding) VALUES (%s, %s);", (doc_id, embedding))
    conn.commit()

# Close connection
cur.close()
conn.close()
