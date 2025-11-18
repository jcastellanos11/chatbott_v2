# chatbott_v2
# 🤖 Chatbot de Documentación – Orfeo / SGDEA

Este proyecto implementa un **chatbot inteligente** capaz de responder preguntas técnicas sobre el sistema **Orfeo–SGDEA (Sistema de Gestión Documental Electrónico y de Archivo)** a partir de su documentación en PDF y repositorios asociados.

El asistente utiliza **LangChain**, **FastAPI**, **ChromaDB** y la API de **OpenAI**, con soporte OCR en español gracias a **unstructured**.

---

## 🚀 Características principales

- ✅ Procesa manuales en PDF con texto e imágenes (OCR incluido).
- 🧠 Genera embeddings vectoriales con **OpenAI (`text-embedding-3-large`)**.
- 📚 Responde preguntas en **español técnico** basándose únicamente en el contenido del documento.
- 🧩 Arquitectura modular (servicios, rutas y utilidades separadas).
- 💬 API REST lista para probar en Postman o integrarse en un front-end React/Streamlit.
- 🪄 Soporte completo para documentos largos (fragmentación automática en “chunks”).
- 🌐 Persistencia local con **ChromaDB** para búsquedas semánticas rápidas.

---

## 🧱 Estructura del proyecto

```
chatbot2/
│
├── app/
│   ├── main.py                     # Punto de entrada FastAPI
│   ├── routes/
│   │   └── chat.py                 # Endpoint principal del chatbot
│   ├── services/
│   │   ├── openai_service.py       # Lógica del modelo, OCR y embeddings
│   ├── utils/
│   │   └── config.py               # Variables de entorno
│   └── __init__.py
│
├── data/
│   ├── pdfs/                       # Carpeta de entrada de PDFs
│   └── vector_db/                  # Base vectorial persistente (Chroma)
│
├── .env                            # Configuración (API Key, rutas, etc.)
├── requirements.txt                # Dependencias del proyecto
└── README.md                       # Este archivo
```

---

## ⚙️ Requisitos previos

- Python ≥ 3.10  
- Clave válida de [OpenAI API](https://platform.openai.com/account/api-keys)
- Tesseract OCR (con soporte en español)

### Instalar Tesseract (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-spa poppler-utils libmagic1
```

---

## 🧩 Instalación

# sudo pacman -Syu tesseract tesseract-data-spa tesseract-data-eng

1. **Clona el repositorio y entra al proyecto**

   ```bash
   git clone https://github.com/tuusuario/chatbot-sgdea.git
   cd chatbot2
   ```

2. **Crea y activa un entorno virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate   # (Windows: venv\Scripts\activate)
   ```

   rm -rf data/vector_db

3. **Instala las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno (.env)**

   ```
   OPENAI_API_KEY=sk-XXXX
   PDF_PATH=./data/pdfs
   VECTOR_DB_PATH=./data/vector_db
   ```

5. **Coloca tus archivos PDF en `data/pdfs/`**

---

## ▶️ Ejecución

Inicia el servidor de desarrollo con:

```bash
uvicorn app.main:app --reload
```

Verás algo como:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
🔄 Creando nueva base vectorial desde PDFs...
📄 Documentos cargados: 1
✂️ Fragmentos creados: 391
✅ Base vectorial creada y guardada.
```

---

## 💬 Uso (vía Postman o cURL)

**Endpoint:**  
`POST http://127.0.0.1:8000/chat/ask`

**Body (JSON):**

```json
{
  "question": "¿Qué módulos tiene el SGDEA?"
}
```

**Respuesta esperada:**

```json
{
  "answer": "El SGDEA está compuesto por los módulos Archivo, Correspondencia, Radicación y Administración..."
}
```

---

## 🧠 Estructura técnica del modelo

- **Loader:** `UnstructuredPDFLoader(languages=["spa"])`
- **Splitter:** `RecursiveCharacterTextSplitter(chunk_size=800, overlap=100)`
- **Embeddings:** `text-embedding-3-large`
- **Vector Store:** `ChromaDB` (persistente)
- **LLM:** `ChatOpenAI(gpt-4o-mini)`
- **Prompt:** instrucción en español técnico para limitar las respuestas al contenido del documento

---

## 🧪 Ejemplo de consulta avanzada

```json
{
  "question": "¿Qué conforma el consecutivo de un radicado?"
}
```

**Respuesta (formato Markdown):**

```
El consecutivo de un radicado está compuesto por los siguientes segmentos:

AAAA DD NNNNN T

- AAAA: Año de radicación.
- DD: Código de la dependencia.
- NNNNN: Número consecutivo asignado.
- T: Tipo de radicación.
```

---

## 🔍 Próximas mejoras

- 🧵 Memoria conversacional por sesión.  
- 📄 Respuestas con citas y referencias de página.  
- 🌐 Front-end web en React o Streamlit.  
- ⚡ Caché de respuestas frecuentes.  
- 🧰 Integración con repositorios Git.

---

## 👨‍💻 Autor

**John Janer Castellanos**  
Ingeniero de Sistemas – Proyecto de Maestría  
📍 Bogotá, Colombia  
🧩 [Orfeo-SGDEA](https://orfeo.gov.co/)  

---

## 📜 Licencia

Este proyecto se distribuye bajo la licencia **MIT**, de libre uso y modificación, con atribución al autor original.

---

> 💡 *Desarrollado con FastAPI + LangChain + OpenAI + unstructured — pensado para documentación técnica en español.*
