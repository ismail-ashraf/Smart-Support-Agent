import uuid
from typing import List, Dict, Any
import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentParser:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 50):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def parse_file(self, content: bytes, filename: str) -> List[Dict[str, Any]]:
        text = ""
        if filename.endswith(".pdf"):
            doc = pymupdf.open(stream=content, filetype="pdf")
            for page in doc:
                text += page.get_text()
        else:
            text = content.decode("utf-8")

        return self.chunk_text(text, filename)

    def chunk_text(self, text: str, source_name: str) -> List[Dict[str, Any]]:
        doc_id = str(uuid.uuid4())

        docs = self.text_splitter.create_documents([text])

        chunks = []
        for idx, doc in enumerate(docs):
            chunks.append({
                "doc_id": doc_id,
                "text": doc.page_content,
                "source": source_name,
                "section": "General Section"
            })

        return chunks