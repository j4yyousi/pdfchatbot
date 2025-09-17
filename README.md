## How To Install
Assuming you have docker, git and runing Ubunbtu, ``git clone` this repository then `cd` to project directory and run the following command, make sure `GEMINI_API_KEY` is set to your key:

```
sudo docker build -t pdfchatbot . && sudo docker run \
  -p 8000:8000 \
  -e DEBUG=False \
  -e DJANGO_SECRET_KEY=sekrit \
  -e GEMINI_API_KEY=your_api_key \
  -e LLM_MODEL_NAME=gemini-2.5-flash \
  -e EMBEDDING_MODEL_NAME=models/gemini-embedding-001 \
  -it pdfchatbot
```
You can get a [gemini api key from here](https://ai.google.dev/gemini-api/docs/quickstart)
## Project Architecture

![Project Architecture Diagram](media/RAG_workflow.png)
[Diagram taken from here](https://huggingface.co/learn/cookbook/en/advanced_rag9)

## Demo

![project Demo](media/pdfchatbot_demo.gif)

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

## Some Useful Linux Commands

to unit test: `UNIT_TESTING=TRUE ./manage.py test`  
to find built containers: `sudo docker ps --all`  
to open terminal in container and debug: `sudo docker exec -it container_name bash`  
to delete a container `sudo docker rm container_name`


## Future work
1. [Test chatbot by building an evaluation system](https://huggingface.co/learn/cookbook/en/rag_evaluation) 
1. Using the evaluation system, try other free models from HuggingFace
1. Using the evaluation system, fine tune the RAG system via the paramters shown in the diagram above.

## References
https://huggingface.co/learn/cookbook/en/advanced_rag
https://huggingface.co/spaces/mteb/leaderboard
https://ai.google.dev/gemini-api/docs