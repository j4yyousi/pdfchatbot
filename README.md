## Install Instructions

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

## Env Params
to unit test:
UNIT_TESTING=TRUE ./manage.py test

gemini model name
api_key
device
## References
https://huggingface.co/learn/cookbook/en/advanced_rag