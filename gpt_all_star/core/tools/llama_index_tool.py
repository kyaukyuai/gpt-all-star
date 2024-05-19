from pathlib import Path
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.schema import Document

from gpt_all_star.core.tools.document_chunker import DocumentChunker
from langchain_core.tools import Tool


def llama_index_tool(path: Path) -> Tool:
    def name_metadata_store(filename: str) -> dict:
        return {"filename": filename}

    def update_documents_and_query(query: str) -> str:
        excluded_file_globs = ["./.archive/**/*", "./node_modules/**/*"]
        documents = SimpleDirectoryReader(
            input_dir=str(path.absolute()),
            recursive=True,
            exclude=excluded_file_globs,
            file_metadata=name_metadata_store,
        ).load_data()
        print(f"Loaded {len(documents)} documents")

        chunked_langchain_documents = DocumentChunker.chunk_documents(
            [doc.to_langchain_format() for doc in documents]
        )
        chunked_documents = [
            Document.from_langchain_format(doc) for doc in chunked_langchain_documents
        ]

        index = VectorStoreIndex.from_documents(documents=chunked_documents)

        return str(index.as_query_engine().query(query))

    return Tool(
        name="LlamaIndex",
        func=update_documents_and_query,
        description="Should be used when you want to reference existing source code.",
        return_direct=False,
    )
