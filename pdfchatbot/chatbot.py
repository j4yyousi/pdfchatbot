from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import FAISS, VectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM,\
                         BitsAndBytesConfig, PreTrainedTokenizerBase, PreTrainedModel
from langchain_community.vectorstores.utils import DistanceStrategy
from torch import bfloat16
from django.core.files.uploadedfile import TemporaryUploadedFile , InMemoryUploadedFile
from PyPDF2 import PdfReader
from .settings import TESTING

class ChatBot():
    def __init__(self) -> None:
        self.file_name: str = ""
        self.vector_db: VectorStore
        self.chunk_size_in_tokens: int = 200
        self.EMBEDDING_MODEL_NAME = "thenlper/gte-small"
        self.prompt_template = [
        {
        "role": "system",
        "content": """Using the information contained in the context,
give a comprehensive answer to the question.
Respond only to the question asked, response should be short and relevant to the question.
If the answer cannot be deduced from the context, do not give an answer. Do not mention the context.""",
        },
        {
        "role": "user",
        "content": """Context: 
{context}
---
Now here is the question you need to answer. Keep your answers short.

Question: {question}""",
        },
        ]

        #Greatly reduces VRAM, at a small accuracy cost. Without it VRAM overflows and crashes vscode.
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=bfloat16,
        )

        READER_MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"
        print("loading model...")
        self.model: PreTrainedModel = AutoModelForCausalLM.from_pretrained(READER_MODEL_NAME,
                                                          quantization_config=bnb_config)
        print("loading tokenizer...")
        self.tokenizer: PreTrainedTokenizerBase = AutoTokenizer.from_pretrained(READER_MODEL_NAME)
        print("loading pipeline...")

        self.llm_pipeline = pipeline(
            model=self.model,
            tokenizer=self.tokenizer,
            task="text-generation",
            do_sample=True,
            temperature=0.2,
            repetition_penalty=1.1,
            return_full_text=False,
            max_new_tokens=500,
        )

        self.rag_prompt_template = self.tokenizer.apply_chat_template(  # type: ignore
            self.prompt_template, tokenize=False, add_generation_prompt=True
        )

        print("loading embedding model...")
        self.embedding_model = HuggingFaceEmbeddings(
        model_name=self.EMBEDDING_MODEL_NAME,
        multi_process=True,
        model_kwargs={"device": "cuda"},
        encode_kwargs={"normalize_embeddings": True},
        )

    @property
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
        text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            self.tokenizer,
            chunk_size=self.chunk_size_in_tokens,
            chunk_overlap=int(self.chunk_size_in_tokens / 10),
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

    def answer_with_rag(self, question: str, num_retrieved_docs: int = 5) -> str:
        print("=> Retrieving documents...")
        relevant_docs = self.vector_db.similarity_search(query=question, k=num_retrieved_docs)

        # Build the final prompt
        context = "\nExtracted documents:\n"
        context += "".join([f"Source: {doc.metadata["id"]}:::\n" + doc.page_content for doc in relevant_docs])

        final_prompt = self.rag_prompt_template.format(question=question, context=context)

        print("=> Generating answer...")
        answer = self.llm_pipeline(final_prompt)[0]["generated_text"]

        return answer

if not TESTING:
    chatbot = ChatBot()

def chatbot_is_file_uploaded() -> bool:
    if TESTING:
        return False
    global chatbot
    return chatbot.is_file_uploaded

def chatbot_process_pdf(file: TemporaryUploadedFile | InMemoryUploadedFile) -> None:
    if TESTING:
        return
    global chatbot
    chatbot.create_vector_db_from_pdf(file)

def chatbot_answer(question: str) -> str:
    if TESTING:
        return "test answer"
    global chatbot
    answer = chatbot.answer_with_rag(question)
    return answer
