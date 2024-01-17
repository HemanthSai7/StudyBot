from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

import json
import wandb
import shutil
import warnings
from backend.ingestion import *
from typing import List, Optional

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Embeddings:
    def __init__(self, config):
        self.config = config

    def split_docs(self, documents, chunk_size=1000, chunk_overlap=150):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        docs = text_splitter.split_documents(documents)
        return docs

    def create_vector_store(self, docs):
        embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.config.embeddings,
            model_kwargs={"device": self.config.device},
            encode_kwargs={"normalize_embeddings": self.config.normalize_embeddings}
            # cache_folder = self.config.CACHE_FOLDER
        )

        shutil.rmtree(self.config.vector_DB, ignore_errors=True)

        texts = self.split_docs(docs)

        vector_store = Chroma.from_documents(
            documents=texts, embedding=embeddings, persist_directory=self.config.vector_DB
        )

        print(f"Vector store created.")

        return vector_store

    def log_dataset(self, documents: List[Document], run: "wandb.run"):
        """Log a dataset to wandb

        Args:
            documents (List[Document]): A list of documents to log to a wandb artifact
            run (wandb.run): The wandb run to log the artifact to.
        """
        document_artifact = wandb.Artifact(name="documentation_dataset", type="dataset")
        with document_artifact.new_file("documents.json") as f:
            for document in documents:
                f.write(document.json() + "\n")

        run.log_artifact(document_artifact)

    def log_index(self, vector_store_dir: str, run: "wandb.run"):
        """Log a vector store to wandb

        Args:
            vector_store_dir (str): The directory containing the vector store to log
            run (wandb.run): The wandb run to log the artifact to.
        """
        index_artifact = wandb.Artifact(name="vector_store", type="search_index")
        index_artifact.add_dir(vector_store_dir)
        run.log_artifact(index_artifact)

    def ingest_data(self, docs):
        vector_store = self.create_vector_store(docs)

        return vector_store


# with open("config.yml", "r", encoding="utf8") as ymlfile:
#     config = box.Box(yaml.safe_load(ymlfile))
# emb = Embeddings(config) 

# docs=PDFDataLoader(config.DATA_PATH).load()
# emb.store_embeddings(docs)
