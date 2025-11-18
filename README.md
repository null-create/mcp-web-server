# **Web Search MCP Server**

A fully local, API-key-free **Web Search MCP (Model Context Protocol) Server** powered by multiple backend providers including DuckDuckGo, Wikipedia, and GitHub’s public search API.
This server exposes search capabilities via **FastMCP** tools, making it ideal for LLM agents, automation systems, or local assistants.

---

## **✨ Features**

- **No API keys required** — uses DuckDuckGo, Wikipedia, and GitHub public endpoints.
- **Unified search API** via MCP tools:

  - `web_search` – general web search
  - `news_search` – news articles
  - `image_search` – image search
  - `video_search` – video search
  - `search_wikipedia` – Wikipedia articles
  - `search_github` – GitHub repositories
  - `get_search_suggestions` – autocomplete suggestions

- **Local HTTP MCP server** provided by FastMCP
- Simple deployment via Python or Docker

---

## **📁 Project Structure**

```
├── .env.example         # Example .env file
├── .gitignore           # git helper
├── Dockerfile           # Docker file for local deployment
├── LICENCE              # Licence file
├── Makefile             # Dev helpers (venv setup, Docker compose, cleanup)
├── README.md            # This file
├── __init__.py          # Python init file
├── docker-compose.yml   # Docker compose file
├── requirements.txt     # Python dependencies
├── search_backends.py   # Search backend implementations (DuckDuckGo, Wikipedia, GitHub)
└── server.py            # MCP server and tool definitions
```

---

## **🚀 Getting Started**

### **Prerequisites**

- Python **3.10+**
- (Optional) `make`
- (Optional) Docker + docker-compose

---

## **🔧 Installation**

### **Option 1: Local Python environment**

```bash
make init
```

Or manually:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## **▶️ Running the MCP Server**

### **Start the server**

```bash
python server.py
```

By default it runs at:

```
HOST: 0.0.0.0
PORT: 9393
```

Override with environment variables:

```bash
export HOST_ADDRESS=127.0.0.1
export HOST_PORT=8080
python server.py
```

---

## **🐳 Running with Docker Compose**

```bash
make dev-compose
```

Stop the environment:

```bash
make dev-down
```

---

## **🧰 MCP Tools Overview**

### **1. `web_search`**

General DuckDuckGo web search.

**Arguments:**

| Name        | Type | Description                 |
| ----------- | ---- | --------------------------- |
| query       | str  | Search query                |
| max_results | int  | 1–50                        |
| region      | str  | e.g. `us-en`, `wt-wt`       |
| safesearch  | str  | `strict`, `moderate`, `off` |

---

### **2. `news_search`**

Searches recent news articles.

**Extra argument:**

- `time_range` – `d`, `w`, `m`, `y`

---

### **3. `image_search`**

DuckDuckGo image search.

**Extra arguments:**

- `size` – Small/Medium/Large/Wallpaper
- `type_image` – photo/clipart/gif/line/transparent

---

### **4. `video_search`**

DuckDuckGo video search.

**Extra arguments:**

- `duration` – Short/Medium/Long
- `resolution` – High/Standard

---

### **5. `search_wikipedia`**

Search Wikipedia and retrieve summaries + URLs.

---

### **6. `search_github`**

Search GitHub repositories via the public API.
No API key required.

---

### **7. `get_search_suggestions`**

Returns DuckDuckGo autocomplete suggestions.

---

## **🧠 Search Backends**

All backend logic is implemented in
`search_backends.py`

Backends include:

- `ddgs` – DuckDuckGo search/text/news/images/videos/suggestions
- `wikipedia` – Wikipedia API wrapper
- GitHub public repository search (REST)

All requests include a custom User-Agent to reduce throttling.

---

## **⚙️ Environment Variables**

| Variable       | Default   | Description  |
| -------------- | --------- | ------------ |
| `HOST_PORT`    | `9393`    | Server port  |
| `HOST_ADDRESS` | `0.0.0.0` | Bind address |

Example:

```bash
HOST_PORT=8080 HOST_ADDRESS=127.0.0.1 python server.py
```

---

## **🧑‍💻 Development**

Initialize local venv:

```bash
make init
```

Clean development environment:

```bash
make clean
```

---

## **🐞 Troubleshooting**

### **I get DuckDuckGo throttling errors**

DuckDuckGo sometimes rate-limits requests.
Try:

- Slower request frequency
- Changing IP
- Avoiding rapid repeated queries

### **GitHub returns 403**

GitHub rate-limits unauthenticated requests.
Wait for reset or reduce frequency.

---

## **📜 License**

MIT
