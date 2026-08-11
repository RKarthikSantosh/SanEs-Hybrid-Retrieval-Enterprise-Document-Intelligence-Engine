from app.llm.groq_llm import get_llm

llm = get_llm()

response = llm.invoke(
    "Explain what Retrieval Augmented Generation is in two sentences."
)

print(response.content)
