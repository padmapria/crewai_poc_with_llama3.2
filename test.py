from langchain_community.llms import Ollama
llm = Ollama(model="llama3.2:1b")
print(llm.invoke("What is 2+2?")) 