# Role-Based Agentic RAG System for Retail

This repository implements a **Role-Based Retrieval-Augmented Generation (RAG) agent** for retail organizations. The system delivers **role-aware, data-grounded customer insights** by combining semantic search, Large Language Models (LLMs), and agentic orchestration.

---

## Key Features

- Role-aware insight generation (Store, Regional, Executive)
- Retrieval-Augmented Generation to reduce hallucinations
- Metadata-driven access control and filtering
- Stateful, graph-based agent orchestration

---

## System Components

- **Data Ingestion & Preprocessing**
  - Cleans and normalizes customer reviews and feedback
  - Enriches data with metadata (store, region, sentiment)

- **Vector Database**
  - Stores embeddings with metadata
  - Enables semantic similarity search with role-based filtering

- **RAG Pipeline**
  - Retrieves Top-K relevant documents
  - Constructs grounded prompts for the LLM
  - Adapts retrieval depth and context per role

- **Agent**
  - Acts as the orchestration layer
  - Handles query routing, interaction state, and role logic

- **Role Definition**
  - Maps organizational roles to:
    - Data visibility
    - Insight scope
    - Response granularity and tone

---

## Architecture Overview
<img width="622" height="306" alt="image" src="https://github.com/user-attachments/assets/9f073335-ecce-490f-a756-ba2a24f0ab64" />



### End-to-End Flow

1. User submits a natural language query  
2. Agent identifies the user’s role, sentiment, region, store (if provided)
3. RAG retrieves role-filtered context from the vector database  
4. LLM generates a grounded, role-specific response  
5. Output is returned in an appropriate format and abstraction level  

---

### Agent Routing Logic
<img width="1227" height="516" alt="image" src="https://github.com/user-attachments/assets/42011f48-a643-4b2b-bea9-9e3f22e9164c" />


- **Store Manager Node**
  - Store-level issues, customer complaints, actionable insights

- **Regional Manager Node**
  - Cross-store trends, regional comparisons, tactical insights

- **Executive Node**
  - Strategic insights, brand perception, retention trends

All nodes invoke the same RAG pipeline with role-adapted parameters.
<img width="1340" height="296" alt="image" src="https://github.com/user-attachments/assets/f2d1b5f7-cc7f-47f8-bb91-e7c10e9140e0" />


---

## Technical Stack

| Component | Choice |
|--------|------|
| Dataset Size | ~50K customer reviews |
| Data Granularity | Region × Store |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Dimension | 384 |
| Similarity Metric | Cosine |
| Vector DB | Pinecone |
| LLM Inference | Groq |
| LLM Model | openai/gpt-oss-20b |
| Agent Framework | LangGraph |

---

## Design Rationale

- **Sentence-Transformers** for embedding flexibility and data privacy
- **Groq** for fast, lightweight LLM inference
- **Pinecone** for scalable, production-grade vector search
- **LangGraph** for explicit, stateful, role-based agent control

---

## Outcome

This system demonstrates how **agentic, role-adaptive RAG** can transform fragmented retail customer data into **actionable insights** tailored to different decision-making levels—improving relevance, trust, and usability across the organization.

