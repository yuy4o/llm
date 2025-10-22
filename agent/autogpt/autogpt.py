import os
os.environ['SERPAPI_API_KEY'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
serpapi_api_key = os.environ.get("SERPAPI_API_KEY")
print(serpapi_api_key)

from langchain.agents import Tool
from langchain_community.tools.file_management.read import ReadFileTool
from langchain_community.tools.file_management.write import WriteFileTool
from langchain_community.utilities import SerpAPIWrapper
import os

search = SerpAPIWrapper()
tools = [
    Tool(
        name="search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
    WriteFileTool(),
    ReadFileTool(),
]

from langchain.docstore import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Define your embedding model
import os
os.environ['OPENAI_API_KEY'] = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
openai_api_key = os.environ.get("OPENAI_API_KEY")
print(openai_api_key)

embeddings_model = OpenAIEmbeddings()
# Initialize the vectorstore as empty
import faiss

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

from langchain_experimental.autonomous_agents import AutoGPT
from langchain_openai import ChatOpenAI

agent = AutoGPT.from_llm_and_tools(
    ai_name="Tom",
    ai_role="Assistant",
    tools=tools,
    llm=ChatOpenAI(temperature=0),
    memory=vectorstore.as_retriever(),
)
# Set verbose to be true
agent.chain.verbose = True

agent.run(["write a weather report for SF today"])

from langchain_community.chat_message_histories import FileChatMessageHistory

agent = AutoGPT.from_llm_and_tools(
    ai_name="Tom",
    ai_role="Assistant",
    tools=tools,
    llm=ChatOpenAI(temperature=0),
    memory=vectorstore.as_retriever(),
    chat_history_memory=FileChatMessageHistory("chat_history.txt"),
)