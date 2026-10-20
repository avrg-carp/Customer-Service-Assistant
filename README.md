# Customer Service Assistant

Ассистент первой линии для сотрудников банка (колл-центр и менеджеры) на основе RAG.
Конкурс ВТБ «Финтех без границ», трек «Собственная эффективность банка».

Находит информацию в базе знаний / регламентах / тарифах и отвечает со ссылками на источники,
сокращая время поиска и AHT. Реальной БЗ банка нет — используется публичный корпус
(сайты банков, ЦБ, законы); план пилота описывает подключение настоящей БЗ.

## Пайплайн

`rewrite query → hybrid search (Qdrant: dense+sparse, RRF) → rerank (top-5) → prompt → LLM с цитатами → confidence gate / «не нашёл»`

Индексация: `upload → Docling → structure-aware chunks → bge-m3 → Qdrant`.

## Стек

| Слой | Выбор |
|---|---|
| Парсинг | Docling |
| Эмбеддинги | BAAI/bge-m3 |
| Векторная БД | Qdrant (hybrid, payload-фильтры) |
| Реранкер | BAAI/bge-reranker-v2-m3 |
| LLM | OpenAI-compatible: vLLM + Qwen2.5 / T-lite (on-prem), GigaChat (cloud), Ollama (без GPU) |
| Backend | FastAPI + Uvicorn, PostgreSQL |
| Frontend | Streamlit/Gradio → SPA |
| Оценка | golden set, recall@k, MRR, Ragas |

## Структура репозитория

```
├─ docker-compose.yml
├─ .env.example
├─ backend/
│  ├─ app/{main.py, api/, auth/, core/config.py}
│  ├─ rag/{ingest, chunking, embed, retrieve, rerank, prompt, generate, guardrails}.py
│  ├─ llm/{base, openai_compat, gigachat}.py
│  └─ tests/
├─ eval/{golden_set.jsonl, run_retrieval_eval.py, run_ragas.py, results/}
├─ data/{raw/, processed/}
├─ frontend/
└─ docs/{architecture.md, data_protection.md}
```

## API (план)

| Метод | Путь | Назначение |
|---|---|---|
| POST | `/v1/ask` | вопрос → ответ + источники (SSE) |
| POST | `/v1/feedback` | 👍/👎, комментарий |
| POST | `/v1/documents` | загрузка документа, запуск индексации |
| GET | `/v1/documents` | список и версии |
| GET | `/v1/analytics/gaps` | вопросы без ответа (пробелы БЗ) |
| GET | `/health` | healthcheck |

## Статус

Реализован только каркас: `/health`, docker-compose (qdrant, postgres, api), заглушки модулей RAG/LLM.
Остальное — по плану спринтов (S1 — загрузка 31 окт, S2 — 29 ноя, S3 — 8 дек).
