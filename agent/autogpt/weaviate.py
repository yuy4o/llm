import os
import getpass
 
os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key:')

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.documen
from langchain.vectorstores import Milvust_loaders import TextLoader


from langchain.document_loaders import TextLoader
loader = TextLoader('./test.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
 
embeddings = OpenAIEmbeddings()
 
 
vector_db = Milvus.from_documents(
    docs,
    embeddings,
    connection_args={"host": "127.0.0.1", "port": "19530"},
)

docs = vector_db.similarity_search(query)

docs[0]