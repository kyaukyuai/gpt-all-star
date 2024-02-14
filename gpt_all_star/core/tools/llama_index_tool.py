from pathlib import Path

from langchain.agents import Tool
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.schema import Document

from gpt_all_star.core.tools.document_chunker import DocumentChunker
from typing import List, Union, Any
from pathlib import Path


def llama_index_tool(path: Path) -> Tool:
    """
    This file contains the implementation of the LlamaIndexTool, which is used for indexing and querying existing source code.

    The LlamaIndexTool provides functionality to load documents, chunk them into smaller pieces, create an index, and perform queries on the index.

    Usage:
        - Instantiate the LlamaIndexTool with a path to the source code directory.
        - Call the `update_documents_and_query` method with a query string to perform a search.

    Example:
        tool = llama_index_tool(Path('/path/to/source/code'))
        result = tool.update_documents_and_query('search query')

    Note: The LlamaIndexTool excludes certain file globs from indexing, such as files in the .archive and node_modules directories.
    """
    def name_metadata_store(filename: str) -> dict:
        """
        Create metadata for a given filename.

        Args:
            filename (str): The name of the file.

        Returns:
            dict: The metadata dictionary containing the filename.

        Raises:
            None
        """
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
