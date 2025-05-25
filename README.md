<h1 align="center" id="top">🤖✨ Mixture of Idiots Agents with RAG ✨🤖</h1>

<p align="center">
  <strong>Harnessing a Symphony of AI Agents for Intelligent Document Q&A!</strong>
</p>

Welcome to the **Mixture of Idiots Agents with RAG**! This project combines the power of Retrieval-Augmented Generation (RAG) with a custom Mixture of Idiots Agents (MoIA) approach, all orchestrated by LangChain and powered by OpenAI models. Get ready to ask questions from your documents and receive intelligently synthesized answers!

## 📜 Table of Contents

1.  [🤔 The Core Idea: RAG + MoIA = Supercharged Q&A](#core-idea)
2.  [📂 Project Structure: What's Under the Hood?](#project-structure)
3.  [🧠 Inside the RAG & MoIA Pipeline](#pipeline-deep-dive)
    *   [📚 `knowledge_vault.py`: Building the Brain](#knowledge-vault)
    *   [💎 `vector_prism.py`: Crafting Document Embeddings](#vector-prism)
    *   [🎼 `ensemble_core.py`: The Orchestra of Agents](#ensemble-core)
    *   [🗣️ `conductor_chain.py`: The MoIA Conductor](#conductor-chain)
    *   [❓ `moa_query.py`: Asking the Smart Questions](#moa-query)
    *   [🧩 Utility Belt: `cipher_decode.py` & `agent_toolkit.py`](#utility-belt)
    *   [🎬 Workflow Diagram](#workflow-diagram)
4.  [🛠️ Tech Stack](#tech-stack)
5.  [🚀 Getting Started: Fire It Up!](#getting-started)
    *   [1. Prerequisites](#prerequisites)
    *   [2. Clone the Repository (If you haven't!)](#clone-repository)
    *   [3. Set Up Your Python Playground (Virtual Environment)](#set-up-virtual-environment)
    *   [4. Install the Magic Spells (Dependencies)](#install-dependencies)
    *   [5. The Secret Key (`.env` file)](#secret-key)
6.  [🏃 How to Run: Let's Go!](#how-to-run)
    *   [🧠 Step 1: Feed the Knowledge Vault](#run-knowledge-vault)
    *   [💬 Step 2: Query the Engine](#run-moa-query)
7.  [✨ Example Output (What to Expect)](#example-output)

---

<h2 id="core-idea">🤔 The Core Idea: RAG + MoIA = Supercharged Q&A</h2>

This project tackles document-based question-answering with a two-pronged strategy:

*   **Retrieval-Augmented Generation (RAG):** We don't just ask a Large Language Model (LLM) a question blindly. First, we search a specialized knowledge base (built from your documents) to find the most relevant text snippets. This context is then *augmented* to the prompt, giving the LLM a solid foundation to base its answer on. This happens in `moa_query.py` when interacting with `ChromaDB`.

*   **Mixture of Idiots Agents (MoIA):** Instead of relying on a single LLM, we employ a team of OpenAI models (`ensemble_core.py`).
    *   **Reference Models:** A set of diverse OpenAI models first generate individual responses to the user's query (which includes the RAG-retrieved context).
    *   **Aggregator Model:** Another, often more powerful, OpenAI model then takes all these initial responses, critically evaluates them, and synthesizes a single, high-quality, and coherent final answer.
    *   This "wisdom of the crowd" (or perhaps, "symphony of specialized agents") approach allows for more robust and nuanced answers.

By combining RAG with MoIA, we aim for answers that are not only contextually grounded in your documents but also refined through multiple AI perspectives.

<h2 id="project-structure">📂 Project Structure: What's Under the Hood?</h2>

Here's a map of your intelligent query system:

```
langchain-moa-rag/
├── .git/                     # Git's magic scroll
├── .gitignore                # Tells Git what to ignore (like secrets!)
├── .venv/                    # Your Python virtual sandbox (GITIGNORED!)
├── data/                     # Folder to store your PDF documents for the knowledge base
├── chroma/                   # Directory where ChromaDB stores its vector index (GITIGNORED!)
├── ensemble_core.py          # Core MoIA logic orchestrating OpenAI agents 🎼
├── conductor_chain.py        # Custom LangChain LLM class for the MoIA 🗣️
├── knowledge_vault.py        # Script to build and populate the knowledge base 📚
├── moa_query.py              # Main script to ask questions using RAG & MoIA ❓
├── vector_prism.py           # Generates text embeddings using OpenAI 💎
├── cipher_decode.py          # Utility for parsing LLM outputs (e.g., for agent functions) 🧩
├── agent_toolkit.py          # Placeholder for custom agent tools 🛠️
├── requirements.txt          # List of Python spells (dependencies)
├── .env                      # Your secret OpenAI API key scroll (GITIGNORED!)
└── README.md                 # This enlightening guide!
```

<h2 id="pipeline-deep-dive">🧠 Inside the RAG & MoIA Pipeline</h2>

Let's peek into the main components:

<h3 id="knowledge-vault">📚 `knowledge_vault.py`: Building the Brain</h3>

*   **Purpose:** This script is responsible for creating your project's long-term memory.
*   **How it Works:**
    1.  Scans the `data/` directory for PDF files.
    2.  Loads and splits the documents into manageable chunks.
    3.  Uses `vector_prism.py` to convert these chunks into numerical representations (embeddings).
    4.  Stores these embeddings in a `ChromaDB` vector database (in the `chroma/` directory).

<h3 id="vector-prism">💎 `vector_prism.py`: Crafting Document Embeddings</h3>

*   **Purpose:** Translates text into a language LLMs understand – vectors!
*   **How it Works:** Uses OpenAI's embedding models (e.g., `text-embedding-ada-002`) to generate vector embeddings for text chunks. This is crucial for finding relevant documents.

<h3 id="ensemble-core">🎼 `ensemble_core.py`: The Orchestra of Agents</h3>

*   **Purpose:** This is the heart of the Mixture of Idiots Agents (MoIA) model.
*   **How it Works:**
    1.  Defines a list of `reference_models` (e.g., `gpt-4o-mini`, `gpt-3.5-turbo`).
    2.  Defines an `aggregator_model` (e.g., `gpt-4.5-preview`).
    3.  When a query comes in (with RAG context), it first sends it to all `reference_models`.
    4.  It then collects their responses and feeds them, along with the original query, to the `aggregator_model`.
    5.  The `aggregator_model`, guided by a system prompt, synthesizes the final answer.

<h3 id="conductor-chain">🗣️ `conductor_chain.py`: The MoIA Conductor</h3>

*   **Purpose:** Integrates the MoIA logic (`ensemble_core.py`) into the LangChain framework by creating a custom LLM class (`moiaChat`).
*   **How it Works:** This class acts as a standard LangChain LLM component, but its internal `_call` method triggers the MoIA process.

<h3 id="moa-query">❓ `moa_query.py`: Asking the Smart Questions</h3>

*   **Purpose:** The main entry point for interacting with your RAG + MoIA system.
*   **How it Works:**
    1.  Takes your question.
    2.  Performs a similarity search in the `ChromaDB` (built by `knowledge_vault.py`) to find relevant document chunks.
    3.  Constructs a prompt that includes your original question and the retrieved context.
    4.  Uses the `moiaChat` LLM (from `conductor_chain.py`) via a LangChain AgentExecutor to get the final, MoIA-synthesized answer.
    5.  Prints the final output.

<h3 id="utility-belt">🧩 Utility Belt: `cipher_decode.py` & `agent_toolkit.py`</h3>

*   `cipher_decode.py`: Provides an output parser, useful if you extend the system to use OpenAI functions or more complex agent interactions.
*   `agent_toolkit.py`: A place to define custom tools if you decide to give your LangChain agent more capabilities beyond Q&A.

<h3 id="workflow-diagram">🎬 Workflow Diagram</h3>

```text
+-----------------+     +----------------------+     +-------------------------+
| User Query      | --> | moa_query.py         | --> | ChromaDB (Vector Store) |
+-----------------+     | - Retrieve Context   |     | (via vector_prism.py)   |
                        +----------------------+     +-------------------------+
                                |         ^          (Built by knowledge_vault.py)
                                | (Query + Context)
                                v
                      +----------------------+
                      | conductor_chain.py   |
                      | (moiaChat LLM)        |
                      +----------------------+
                                |
                                v
                      +----------------------+
                      | ensemble_core.py     |
                      | - Reference Models   | ----> [GPT-3.5, GPT-4o-mini, ...]
                      | - Aggregator Model   | ----> [GPT-4.5-preview]
                      +----------------------+
                                |
                                v
                      +----------------------+
                      | Final Synthesized    |
                      | Answer to User       |
                      +----------------------+
```

---

<h2 id="tech-stack">🛠️ Tech Stack</h2>

*   **Python 3.x**
*   **LangChain:** The core framework for orchestrating the pipeline.
*   **OpenAI API:** Powering the LLM agents (both reference and aggregator) and embeddings.
*   **ChromaDB:** For local vector storage and retrieval.
*   **python-dotenv:** For managing your precious API keys securely.

<h2 id="getting-started">🚀 Getting Started: Fire It Up!</h2>

Follow these steps to get this intelligent query engine humming on your machine.

<h3 id="prerequisites">1. Prerequisites</h3>

*   Python 3.8 or higher.
*   `pip` (Python package installer).

<h3 id="clone-repository">2. Clone the Repository (If you haven't!)</h3>

If you don't have the project files yet:
```bash
git clone https://github.com/VinsmokeSomya/Mixture-of-Idiots-Agents-with-RAG.git
cd Mixture-of-Idiots-Agents-with-RAG
```

<h3 id="set-up-virtual-environment">3. Set Up Your Python Playground (Virtual Environment)</h3>

Keep your global Python environment clean by using a virtual one for this project:
```bash
python -m venv .venv
```
Activate it:
*   **On Windows (PowerShell/CMD):**
    ```bash
    .venv\Scripts\activate
    ```
*   **On macOS/Linux (bash/zsh):**
    ```bash
    source .venv/bin/activate
    ```
    Your terminal prompt should now start with `(.venv)`.

<h3 id="install-dependencies">4. Install the Magic Spells (Dependencies)</h3>

With your virtual environment active, conjure the necessary packages:
```bash
pip install -r requirements.txt
```

<h3 id="secret-key">5. The Secret Key (`.env` file)</h3>

1.  You'll need an API key from [OpenAI](https://platform.openai.com/api-keys).
2.  In the root directory of the project, create a file named `.env`.
3.  Add your OpenAI API key to this `.env` file like so:
    ```env
    OPENAI_API_KEY="your_actual_openai_api_key_here"
    ```
    This file is listed in `.gitignore`, so your key won't accidentally be shared.

<h2 id="how-to-run">🏃 How to Run: Let's Go!</h2>

<h3 id="run-knowledge-vault">🧠 Step 1: Feed the Knowledge Vault</h3>

1.  Place your PDF documents into the `/data` directory.
2.  Run the script to process these documents and build the vector database:
    ```bash
    python knowledge_vault.py
    ```
    You can add the `--reset` flag if you want to clear an existing database before populating: `python knowledge_vault.py --reset`

<h3 id="run-moa-query">💬 Step 2: Query the Engine</h3>

Once the knowledge vault is ready, you can start asking questions:
```bash
python moa_query.py
```
You can change the default question inside the `moa_query.py` script.

<h2 id="example-output">✨ Example Output (What to Expect)</h2>

When you run `python moa_query.py`, you'll see logs in your terminal showing:
*   Initialization of the MoIA chain (`construct MOA`).
*   Calls to each reference model (e.g., `Model: gpt-4o-mini, Role: Reference`).
*   A marker for the final aggregation step (`--- Running Final Aggregation Layer ---`).
*   The call to the aggregator model (e.g., `Model: gpt-4.5-preview, Role: Aggregator`).
*   And finally, the synthesized answer to your query!

Example for a query like "How much money does a player start with in Monopoly?":
```
construct MOA
Model: gpt-4o-mini, Role: Reference
Model: gpt-4.5-preview-2025-02-27, Role: Reference
...
--- Running Final Aggregation Layer ---
Model: gpt-4.5-preview, Role: Aggregator
1500
```

---

Happy Querying! 🚀

