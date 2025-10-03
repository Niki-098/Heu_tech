from retriever import Retriever
from reasoner import Reasoner
from actor import Actor

def run_pipeline(query):
    retriever = Retriever()
    reasoner = Reasoner()
    actor = Actor()

    # Step 1: Retrieve KB context
    results = retriever.search(query)
    context = " ".join([text for _, text in results])
    print(f"Retrieved context: {context[:100]}...")  # Debug: Show first 100 chars of context

    # Step 2: LLM reasoning
    reasoning = reasoner.reason(query, context)
    print("Reasoner Decision:", reasoning)

    # Step 3: If API call, execute actor
    if "API_CALL:" in reasoning:
        topic = reasoning.split("API_CALL:")[1].strip()
        api_result = actor.call_api(topic)
        print(f"API Result: {api_result}")
        return {
            "query": query,
            "result": api_result["answer"],
            "source": api_result["source"],
            "log": reasoning
        }
    else:
        return {
            "query": query,
            "result": reasoning,
            "source": "knowledge_base_summarized",
            "log": "Answered from KB"
        }