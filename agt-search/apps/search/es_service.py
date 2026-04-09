"""AGT Search Service v1.0 - Elasticsearch client service."""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_es():
    try:
        from elasticsearch import Elasticsearch
        return Elasticsearch(getattr(settings, "ELASTICSEARCH_URL", "http://localhost:9200"))
    except Exception as e:
        logger.error(f"ES connection failed: {e}")
        return None


class ESService:

    @classmethod
    def create_index(cls, index_name, schema_fields):
        es = _get_es()
        if not es:
            return False
        properties = {}
        for f in schema_fields:
            ft = f["field_type"]
            if ft == "text":
                mapping = {"type": "text"}
                if f.get("autocomplete"):
                    mapping["fields"] = {"autocomplete": {"type": "text", "analyzer": "autocomplete_analyzer"}}
            elif ft == "keyword":
                mapping = {"type": "keyword"}
            elif ft == "number":
                mapping = {"type": "float"}
            elif ft == "date":
                mapping = {"type": "date"}
            elif ft == "boolean":
                mapping = {"type": "boolean"}
            else:
                mapping = {"type": "text"}
            properties[f["field_name"]] = mapping

        body = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "autocomplete_analyzer": {
                            "type": "custom", "tokenizer": "standard",
                            "filter": ["lowercase", "autocomplete_filter"]
                        }
                    },
                    "filter": {
                        "autocomplete_filter": {"type": "edge_ngram", "min_gram": 2, "max_gram": 20}
                    }
                }
            },
            "mappings": {"properties": properties}
        }
        try:
            es.indices.create(index=index_name, body=body, ignore=400)
            return True
        except Exception as e:
            logger.error(f"ES create index failed: {e}")
            return False

    @classmethod
    def index_document(cls, index_name, doc_id, data):
        es = _get_es()
        if not es:
            return False
        try:
            es.index(index=index_name, id=doc_id, body=data)
            return True
        except Exception as e:
            logger.error(f"ES index doc failed: {e}")
            return False

    @classmethod
    def delete_document(cls, index_name, doc_id):
        es = _get_es()
        if not es:
            return False
        try:
            es.delete(index=index_name, id=doc_id, ignore=404)
            return True
        except Exception as e:
            logger.error(f"ES delete doc failed: {e}")
            return False

    @classmethod
    def search(cls, index_name, query, filters=None, sort=None, page=1, limit=20, fuzzy=True, highlight=True):
        es = _get_es()
        if not es:
            return {"results": [], "total": 0, "took_ms": 0}

        body = {"query": {"bool": {"must": [], "filter": []}}}
        if query:
            match = {"multi_match": {"query": query, "fields": ["*"], "type": "best_fields"}}
            if fuzzy:
                match["multi_match"]["fuzziness"] = "AUTO"
            body["query"]["bool"]["must"].append(match)

        for f in (filters or []):
            op = f.get("operator", "eq")
            if op == "eq":
                body["query"]["bool"]["filter"].append({"term": {f["field"]: f["value"]}})
            elif op == "range":
                r = {}
                if "min" in f:
                    r["gte"] = f["min"]
                if "max" in f:
                    r["lte"] = f["max"]
                body["query"]["bool"]["filter"].append({"range": {f["field"]: r}})

        if sort:
            body["sort"] = [{sort["field"]: {"order": sort.get("order", "desc")}}]

        if highlight:
            body["highlight"] = {"fields": {"*": {}}}

        body["from"] = (page - 1) * limit
        body["size"] = limit

        try:
            resp = es.search(index=index_name, body=body)
            hits = resp.get("hits", {})
            results = []
            for h in hits.get("hits", []):
                r = {"doc_id": h["_id"], "score": h.get("_score"), "data": h.get("_source", {})}
                if "highlight" in h:
                    r["highlights"] = h["highlight"]
                results.append(r)
            return {"results": results, "total": hits.get("total", {}).get("value", 0),
                    "took_ms": resp.get("took", 0), "page": page, "limit": limit}
        except Exception as e:
            logger.error(f"ES search failed: {e}")
            return {"results": [], "total": 0, "took_ms": 0}

    @classmethod
    def autocomplete(cls, index_name, prefix, limit=8):
        es = _get_es()
        if not es:
            return []
        try:
            body = {"query": {"multi_match": {"query": prefix, "type": "phrase_prefix", "fields": ["*"]}}, "size": limit}
            resp = es.search(index=index_name, body=body)
            return [{"text": h["_source"].get("title") or h["_source"].get("name") or list(h["_source"].values())[0],
                     "doc_id": h["_id"]} for h in resp.get("hits", {}).get("hits", [])]
        except Exception as e:
            logger.error(f"ES autocomplete failed: {e}")
            return []

    @classmethod
    def bulk_operations(cls, index_name, operations):
        es = _get_es()
        if not es:
            return {"succeeded": 0, "failed": len(operations), "errors": []}
        succeeded = failed = 0
        errors = []
        for op in operations:
            try:
                if op["action"] == "index":
                    es.index(index=index_name, id=op["doc_id"], body=op.get("data", {}))
                    succeeded += 1
                elif op["action"] == "delete":
                    es.delete(index=index_name, id=op["doc_id"], ignore=404)
                    succeeded += 1
            except Exception as e:
                failed += 1
                errors.append({"doc_id": op.get("doc_id"), "error": str(e)[:200]})
        return {"total": len(operations), "succeeded": succeeded, "failed": failed, "errors": errors}

    @classmethod
    def delete_index(cls, index_name):
        es = _get_es()
        if not es:
            return False
        try:
            es.indices.delete(index=index_name, ignore=404)
            return True
        except Exception as e:
            logger.error(f"ES delete index failed: {e}")
            return False
