# ranker.py
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')  # small <90MB

def rank_sections(sections, persona):
    job_context = f"{persona['role']} needs to {persona['job']}"
    job_emb = model.encode(job_context, convert_to_tensor=True)

    ranked = []
    for section in sections:
        score = util.cos_sim(model.encode(section["title"], convert_to_tensor=True), job_emb)
        ranked.append((score.item(), section))
    
    ranked.sort(reverse=True, key=lambda x: x[0])
    return [s[1] for s in ranked[:5]]
