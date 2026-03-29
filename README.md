# Political Recommendation System

Instead of making keywords, the system will try to extract values and align them with party programs. 

The idea is to make a RAG:
1. Take the PDFs programs from:
    - Partido Popular (PP).
    - Partido Socialista Obrero Español (PSOSE).
    - Vox.
    - Sumar.
    - Podemos.
2. Convert them into text.
3. Chunk them. 
4. Store Embeddings.
5. Query them dynamically.

## Idea:

Instead of asking "Which party do you like?", we try to understand your values
first and then exaplain how they align with the different parties.

## Architecture

1. Data Ingestion:

    1. PDF -> Text
    2. Clean + Chunk.
    3. Store in Vector DB

2. Question Generator Agent: Generates questions like:
    - Taxes vs public spending.
    - Immigration policy.
    - EU integration. 
    - Climate regulation.
    - Labor laws.

3. Interviewer Agent
    The idea is that those questions should differenciate parties, and the agent
    ask them in an interactive way (by console). The result of this step would
    be a JSON like this one:

    ```json
    {
        "taxes": "low",
        "immigration": "restrictive",
        "climate": "moderate",
        "labor": "pro-worker"
    }
    ```

4. Matching / Scoring Agent

Here we have 2 options: 

Options A (simple):
1. Embed user answers.
2. Compare user answers with party program embeddings.
3. Rank Similarity

Option B (more interesting):
For each party ask: "Given this user profile, how aligned is this part (0-10)? Explain"


Option B is more slower, but much richer because the system won't tell you just
the party "You match PSOE", but rather something like "You align 78% with PSOE
because":
- You support X
- They propose Y
- You differ on Z

## Potential Criticisms

1. Bias: LLMs might interpret programs incorrectly.
2. Oversimplification: politics is complex.
3. Programs are not reality. Parties don't always do what they promise. 

## Ideas for future features
- Compare program vs Actual Policies.
- Let user weight topics: Economy 80%, Climate 20%
- Multi Agent debate mode: simulate each party defending your answers.

## Quickstart (prototype)

1. Create a virtual environment and install requirements:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    pip install -r requirements-dev.txt

2. Set your OpenAI key (if using OpenAI):

    export OPENAI_API_KEY=your_key_here

3. Ingest party program PDFs:

    python -m src.main --ingest path/to/pp.pdf path/to/psoe.pdf --persist-dir ./data/chroma

Note: We can find the Spanish political parties plan here: 
https://www.senado.es/web/composicionorganizacion/gruposparlamentarios/programaselectoralespartidos/index.html

I had to research a bit each electoral plan because I couldn't find a webpage
with all the electoral plans.


4. Run the recommendation interview and scoring flow:

    python -m src.main --recommend --persist-dir ./data/chroma

Notes:
- The prototype uses langchain and Chroma for the vector store. If OpenAI is
  not available, the ingestion will attempt a sentence-transformers fallback
  for embeddings (local model).
- This is a minimal starting point. Next steps: add robust parsing, store
  source metadata, implement a question generator agent, and a richer scoring
  pipeline using RAG prompts.


# How to run the app

# create env and install deps
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# set your OpenAI key if you plan to use OpenAI
export OPENAI_API_KEY="sk_..."

# ingest PDFs (example)
python3 -m src.main --ingest path/to/pp.pdf path/to/psoe.pdf --persist-dir ./data/chroma

# run the interview + scoring flow
python3 -m src.main --recommend --persist-dir ./data/chroma







# Download embedding model

Info: https://ollama.com/library/nomic-embed-text

```bash
ollama pull nomic-embed-text
```








