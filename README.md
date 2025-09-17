## How To Install
In Docker setup file:  
gemini llm model name  
gemini embeddings model name  
gemini api_key
## Project Architecture

![Project Architecture Diagram](media/RAG_workflow.png)
[Diagram taken from here](https://huggingface.co/learn/cookbook/en/advanced_rag9)

## Demo



## API Documentation

### **URL:** `/`  
### **Method:** `GET`

### Description
Displays the main page of the application with file upload status and chat messages.

### Returns
- **200 OK**
  Renders the `home_turbo.html` template with the following context:
  - `file_uploaded`: A boolean indicating if a file has been uploaded.
  - `file_name`: The name of the uploaded file, if any.
  - `chat_messages`: A list of dictionaries containing chat messages.
- **405 Method Not Allowed**
  If the request method is not `GET`.

---

### **URL:** `/upload`  
### **Method:** `POST`

### Description
Accepts a PDF file from a form and processes it. The file is expected in the `request.FILES` dictionary under the key `pdf_input`. After processing, it redirects the user back to the home page.

### Returns
- **302 Found**  
  Redirects to the `/` endpoint upon successful file processing.
- **405 Method Not Allowed**  
  If the request method is not `POST`.

---

### **URL:** `/chat`  
### **Method:** `POST`

### Description
Handles chat interactions between the user and the chatbot. Accepts a user's question from a form, appends it to the chat history, and generates a chatbot response. Both the user's question and the chatbot's answer are stored in the messages list.

### Parameters
- `chat_input` *(string)*: The user's question submitted via a form.

### Returns
- **302 Found**  
  Redirects to the `/` endpoint after processing the chat input.
- **405 Method Not Allowed**  
  If the request method is not `POST`.

## tradeoffs
I chose the embeddigns to be on device while llm on cloud since its too big in size and requires gpu.
Without tokenizer the performence gets worse.

Tested on PDFs of 300*50 = 15k characters

## Some Useful Commands

to unit test: `UNIT_TESTING=TRUE ./manage.py test`

## Future work
1. [Test chatbot by building an evaluation system](https://huggingface.co/learn/cookbook/en/rag_evaluation) 
1. Using the evaluation system, try other free models from HuggingFace
1. Using the evaluation system, fine tune the RAG system via the paramters shown in the diagram above.

## References
https://huggingface.co/learn/cookbook/en/advanced_rag
https://huggingface.co/spaces/mteb/leaderboard
https://ai.google.dev/gemini-api/docs