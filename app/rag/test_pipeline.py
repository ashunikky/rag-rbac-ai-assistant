from app.rag.pipeline import rag_pipeline

result = rag_pipeline("revenue", "hr")

print("\nANSWER:\n", result["answer"])
print("\nSOURCES:\n", result["sources"])