from typing import Dict, List

from langchain_openai import ChatOpenAI


def score_parties(
    user_profile: Dict[str, str],
    parties: List[str],
    model_name: str = "gpt-3.5-turbo",
) -> Dict[str, Dict]:
    """For each party, ask the LLM to score alignment 0-100 and provide
    a short explanation. Returns a mapping party -> {score, explanation}.
    """
    llm = ChatOpenAI(model=model_name, temperature=0.0)

    results = {}
    for p in parties:
        prompt = f"""
You are given a user profile describing policy preferences as a JSON:
{user_profile}

Evaluate how well the party '{p}' matches that profile on a scale from 0 to
100. Respond with JSON: {{"score": <int>, "explanation": "..."}}
Give a concise explanation (1-3 sentences).
"""

        resp = llm.invoke(prompt)
        text = resp.content
        # naive parse: try to extract JSON-like substring
        results[p] = {"raw": text}

    return results
