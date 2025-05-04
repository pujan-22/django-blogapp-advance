import re
import math

stopwords = set("""
a an the and or is are was were be been being of in to from for with as by on at
""".split())

def tokenize(sentence):
    words = re.findall(r'\b[a-z]{2,}\b', sentence.lower())
    return [word for word in words if word not in stopwords]

def sentence_similarity(s1, s2):
    words1 = set(tokenize(s1))
    words2 = set(tokenize(s2))
    if not words1 or not words2:
        return 0
    return len(words1 & words2) / (math.log(len(words1) + 1) + math.log(len(words2) + 1))

def build_similarity_matrix(sentences):
    size = len(sentences)
    matrix = [[0.0]*size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if i != j:
                matrix[i][j] = sentence_similarity(sentences[i], sentences[j])
    return matrix

def pagerank(matrix, eps=0.0001, d=0.85):
    size = len(matrix)
    scores = [1.0] * size
    while True:
        prev_scores = scores[:]
        for i in range(size):
            sum_sim = 0
            for j in range(size):
                if matrix[j][i] != 0:
                    out_degree = sum(matrix[j])
                    if out_degree != 0:
                        sum_sim += (matrix[j][i] / out_degree) * prev_scores[j]
            scores[i] = (1 - d) + d * sum_sim
        if max(abs(scores[i] - prev_scores[i]) for i in range(size)) < eps:
            break
    return scores

def summarize_text(text, num_sentences=3):

    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    
    sentences = []
    for para in paragraphs:
        para_sentences = re.split(r'(?<=[.!?]) +', para)
        sentences.extend([s.strip() for s in para_sentences if s.strip()])
        
    if len(sentences) <= num_sentences:
        return text
    sim_matrix = build_similarity_matrix(sentences)
    scores = pagerank(sim_matrix)
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    summary = [s for _, s in sorted(ranked_sentences[:num_sentences], key=lambda x: sentences.index(x[1]))]
    return ' '.join(summary)
