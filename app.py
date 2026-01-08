from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os

app = Flask(__name__, static_folder='.')
CORS(app)

DB_PATH = "./data/apps.json"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5

print("🔄 Loading model...")
model = SentenceTransformer(MODEL_NAME)

print("📁 Loading database...")
with open(DB_PATH, "r", encoding="utf-8") as f:
    db = json.load(f)

apps = db["apps"]

app_embeddings = []
valid_apps = []

for app_data in apps:
    if app_data.get("embedding"):
        app_embeddings.append(app_data["embedding"])
        valid_apps.append(app_data)

app_embeddings = np.array(app_embeddings)
app_embeddings = app_embeddings / np.linalg.norm(
    app_embeddings, axis=1, keepdims=True
)

print(f"✅ Loaded {len(valid_apps)} apps")


def keyword_score(query: str, app_data: dict) -> float:
    query = query.lower()
    text = " ".join([
        app_data.get("name", ""),
        " ".join(app_data.get("aliases", [])),
        " ".join(app_data.get("features", [])),
    ]).lower()
    
    score = 0.0
    for token in query.split():
        if token in text:
            score += 1
    
    return min(score / 5, 1.0)


def category_boost(query: str, app_data: dict) -> float:
    if app_data.get("category", "").lower() in query.lower():
        return 1.0
    return 0.0


def search_apps(query: str, top_k: int = TOP_K):
    query_embedding = model.encode(query)
    query_embedding = query_embedding / np.linalg.norm(query_embedding)
    
    semantic_scores = np.dot(app_embeddings, query_embedding)
    
    results = []
    
    for idx, app_data in enumerate(valid_apps):
        sem_score = float(semantic_scores[idx])
        key_score = keyword_score(query, app_data)
        cat_boost = category_boost(query, app_data)
        
        final_score = (
            0.5 * sem_score +
            0.3 * key_score +
            0.2 * cat_boost
        )
        
        results.append({
            "app": app_data,
            "semantic_score": sem_score,
            "keyword_score": key_score,
            "category_boost": cat_boost,
            "final_score": final_score,
        })
    
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results[:top_k]


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/apps', methods=['GET'])
def get_all_apps():
    return jsonify({
        'apps': valid_apps,
        'total': len(valid_apps)
    })


@app.route('/api/search', methods=['POST'])
def api_search():
    try:
        data = request.get_json()
        query = data.get('query', '')
        top_k = data.get('top_k', TOP_K)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        results = search_apps(query, top_k)
        
        return jsonify({
            'query': query,
            'results': results,
            'total': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 SEO App Search Engine")
    print("="*60)
    print(f"📊 Model: {MODEL_NAME}")
    print(f"📱 Apps: {len(valid_apps)}")
    print(f"🌐 URL: http://localhost:5001")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)