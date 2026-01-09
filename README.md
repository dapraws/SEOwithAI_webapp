# 🔍 SEO with AI — App Version (Semantic Search Engine)

**AI-powered semantic search engine** berbasis **Flask + Sentence Transformers**.

---

## ✨ Features

- 🤖 **Semantic Search (AI-based)**
- 🔎 **Hybrid Search Scoring**
  - 50% Semantic similarity
  - 30% Keyword matching
  - 20% Category boost
- ⚡ **Fast JSON-based search**
- 🌐 **REST API (Flask)**
- 🎨 **Modern UI (Tailwind CSS)**

---

## 🗂 Project Structure

```

SEOwithAI_program/
│
├── data/
│   └── apps.json          # Database aplikasi + embedding
│
├── app.py                 # Flask backend (API + search engine)
├── index.html             # Frontend UI (Tailwind CSS)
├── requirements.txt       # Python dependencies
└── README.md

```

---

## 📄 Data Schema (`data/apps.json`)

```json
{
  "meta": {
    "version": "1.0",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "last_updated": "2026-01-08"
  },
  "apps": [
    {
      "id": "app_001",
      "name": "HR-X9",
      "aliases": ["absensi HR", "attendance app"],
      "category": "Human Resource",
      "description": "Aplikasi absensi karyawan berbasis mobile.",
      "features": ["absensi karyawan", "GPS tracking", "face recognition"],
      "search_text": "...",
      "embedding": [],
      "content_hash": "",
      "status": "active"
    }
  ]
}
```

### 🔑 Important Fields

| Field         | Description                         |
| ------------- | ----------------------------------- |
| `search_text` | Text utama untuk semantic embedding |
| `embedding`   | Vector embedding hasil encoding     |
| `aliases`     | Sinonim / variasi pencarian         |
| `features`    | Keyword pendukung                   |
| `category`    | Digunakan untuk category boosting   |

---

## 🧠 Embedding Model

Menggunakan model open-source:

```
sentence-transformers/all-MiniLM-L6-v2
```

**Kenapa model ini?**

- ⚡ Cepat & ringan
- 📦 Gratis (tanpa API key)
- 🎯 Akurat untuk semantic similarity

---

## ⚙️ Installation (Local)

### 1️⃣ Clone repository

```bash
git clone https://github.com/your-username/SEOwithAI_program.git
cd SEOwithAI_program
```

### 2️⃣ (Optional) Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Run the App

```bash
python app.py
```

Output:

```
🚀 SEO App Search Engine
📊 Model: sentence-transformers/all-MiniLM-L6-v2
📱 Apps: X
🌐 URL: http://localhost:5001
```

Open browser:

```
http://localhost:5001
```

---

## 🧪 Scoring Formula

```python
final_score =
  0.5 * semantic_score +
  0.3 * keyword_score +
  0.2 * category_boost
```

### 🧩 Score Explanation

- **Semantic Score (50%)**
  → AI memahami makna query
- **Keyword Score (30%)**
  → kecocokan literal
- **Category Boost (20%)**
  → Intent & konteks kategori

---
