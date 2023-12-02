from langchain.vectorstores import Qdrant
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

import shutil
import warnings
from backend.ingestion import *

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Embeddings:
    def __init__(self, cfg):
        self.cfg = cfg

    def split_docs(self, documents, chunk_size=1000, chunk_overlap=150):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        docs = text_splitter.split_documents(documents)
        return docs

    def store_embeddings(self, docs):
        embeddings = SentenceTransformerEmbeddings(
            model_name=self.cfg.EMBEDDINGS,
            model_kwargs={"device": self.cfg.DEVICE},
            encode_kwargs={"normalize_embeddings": self.cfg.NORMALIZE_EMBEDDINGS},
        )

        shutil.rmtree(self.cfg.VECTOR_DB, ignore_errors=True)

        texts = self.split_docs(docs)

        vector_store = Qdrant.from_documents(
            texts,
            embeddings,
            # path=self.cfg.VECTOR_DB,
            location=":memory:",
            # host="localhost",
            # prefer_grpc=True,
            collection_name=self.cfg.VECTOR_DB
        )

        print(f"Vector store created at {self.cfg.VECTOR_DB}")

        return vector_store


# with open("config.yml", "r", encoding="utf8") as ymlfile:
#     cfg = box.Box(yaml.safe_load(ymlfile))
# emb = Embeddings(cfg)

# docs=PDFDataLoader(cfg.DATA_PATH).load()
# emb.store_embeddings(docs)
