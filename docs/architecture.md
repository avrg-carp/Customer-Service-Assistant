# Архитектура

## Пайплайн запроса
`rewrite → hybrid search (dense top-30 + sparse top-30 → RRF; фильтры allowed_roles, valid_to в Qdrant) → rerank top-5 → prompt → LLM с цитатами [n] → confidence gate`

## Контроль качества ответа
- порог reranker-score → «не нашёл» без вызова LLM
- temperature 0–0.2
- проверка, что каждый `[n]` указывает на реальный фрагмент

## Qdrant payload
`doc_id, title, section, page, url, product, segment, topic, valid_from, valid_to, version, allowed_roles, hash`

Обновление: инкрементальная переиндексация по hash; старые версии помечаются невалидными.

## Чанкинг
По заголовкам/абзацам, 300–600 токенов, overlap 10–15%; таблицы целиком с заголовком; префикс «документ/раздел».
