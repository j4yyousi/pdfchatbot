from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import FAISS, VectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy
from django.core.files.uploadedfile import TemporaryUploadedFile , InMemoryUploadedFile
from PyPDF2 import PdfReader
from .settings import UNIT_TESTING
from google import genai
from google.genai import types

class VectorDb():
    def __init__(self) -> None:
        self.file_name: str = ""
        self.vector_db: VectorStore
        self.chunk_size_in_chars: int = 200

        EMBEDDING_MODEL_NAME = "thenlper/gte-small"
        print("loading embedding model...")
        self.embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        multi_process=True,
        #model_kwargs={"device": "cuda"},
        encode_kwargs={"normalize_embeddings": True},
        )

    def is_file_uploaded(self) -> bool:
        return bool(self.file_name)

    def convert_to_document(self, file: TemporaryUploadedFile | InMemoryUploadedFile) -> list[Document]:
        raw_knowledge_base: list[Document] = []
        self.file_name = file.name
        reader = PdfReader(file)
        for i in range(len(reader.pages)):
            raw_knowledge_base.append(Document(page_content=reader.pages[i].extract_text(), metadata={"page": i + 1}))
        return raw_knowledge_base

    def split_document_into_chunks(self, raw_knowledge_base: list[Document]) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size_in_chars,
            chunk_overlap=int(self.chunk_size_in_chars / 10),
            add_start_index=True,
            strip_whitespace=True,
            separators=["\n\n", "\n", ".", " "],
        )
        print("at text splitting...")
        chunks = text_splitter.split_documents(raw_knowledge_base)
        return chunks

    def calculate_chunk_ids(self, chunks: list[Document]) -> list[Document]:
        # This will create IDs like "file_name.pdf:6:2"
        # Page Source : Page Number : Chunk Index
        print(f"calculating chunk ids...")
        last_page_id = None
        current_chunk_index = 0
        for chunk in chunks:
            page = chunk.metadata.get("page")
            current_page_id = f"{page}"

            # If the page ID is the same as the last one, increment the index.
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            # Calculate the chunk ID.
            chunk_id = f"page:{current_page_id}&chunk:{current_chunk_index}"
            last_page_id = current_page_id

            # Add it to the page meta-data.
            chunk.metadata["id"] = chunk_id

        return chunks

    def create_vector_db_from_pdf(self, file: TemporaryUploadedFile | InMemoryUploadedFile):
        raw_knowledge_base: list[Document] = self.convert_to_document(file)
        chunks: list[Document] = self.split_document_into_chunks(raw_knowledge_base)
        chunks = self.calculate_chunk_ids(chunks)
        print("creating vector db...")
        self.vector_db = FAISS.from_documents(
            chunks, self.embedding_model, distance_strategy=DistanceStrategy.COSINE
        )

class ChatBotCloud(VectorDb):
    def __init__(self):
        super().__init__()
        self.llm_client = genai.Client()

    def build_context(self, question: str, num_docs: int = 5):
        print("=> Retrieving documents...")
        relevant_docs = self.vector_db.similarity_search(query=question, k=num_docs)

        # Build the final prompt
        context = "\nExtracted documents:\n"
        context += "".join([f"Source: {doc.metadata["id"]}\n" + doc.page_content for doc in relevant_docs])
        return context

    def build_user_prompt(self, question: str):
        context = self.build_context(question)
        user_template = """Context: 
{context}
---
Now here is the question you need to answer. Keep your answers short.

Question: {question}"""
        user_prompt = user_template.format(question=question, context=context)
        return user_prompt

    def answer_with_rag(self, question: str) -> str:
        system_prompt = """Using the information contained in the context,
give a comprehensive answer to the question.
Respond only to the question asked, response should be short and relevant to the question.
If the answer cannot be deduced from the context, do not give an answer."""
        user_prompt = self.build_user_prompt(question)

        print("=> Generating answer...")
        try:
            answer = self.llm_client.models.generate_content(
                model="gemini-2.5-pro",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt),
                contents=user_prompt,
            )
        except Exception as e:
            print("Unexpected error:", e)
            return f"Could not get answer from remote LLM. Error message: {e}"

        return answer.text

if not UNIT_TESTING:
    chatbot = ChatBotCloud()

def chatbot_is_file_uploaded() -> bool:
    if UNIT_TESTING:
        return False
    global chatbot
    return chatbot.is_file_uploaded()

def chatbot_get_file_name() -> str:
    if UNIT_TESTING:
        return "test.pdf"
    global chatbot
    return chatbot.file_name

def chatbot_process_pdf(file: TemporaryUploadedFile | InMemoryUploadedFile) -> None:
    if UNIT_TESTING:
        return
    global chatbot
    chatbot.create_vector_db_from_pdf(file)

def chatbot_answer(question: str) -> str:
    if UNIT_TESTING:
        return "test answer"
    global chatbot
    answer = chatbot.answer_with_rag(question)
    return answer
