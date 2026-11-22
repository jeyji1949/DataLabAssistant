# DataLabAssistant

A small Python project that turns messy lab instrument files into clean, queryable data, and lets you ask questions about it in plain language with a local LLM.

> **Status: work in progress.** The parsing, validation, storage, API, web interface and LLM assistant work locally. Docker packaging and LLM evaluation are the next steps (see [Roadmap](#roadmap)).

## The problem

Plate-reader exports (growth curves of bacterial strains, for example) are often messy: inconsistent headers, missing values, mixed formats. Before any analysis, someone has to clean them by hand.

This project automates that path: **messy file → validated data → API → question in natural language → answer.**

## What it does

1. **Parses** a messy plate-reader CSV with `pandas`.
2. **Validates** every row with `pydantic` (types, ranges, required fields), so bad data is caught early.
3. **Stores** the clean data in SQLite / JSON.
4. **Analyses** it with simple functions (summary per strain, fastest-growing strain, ...), covered by `pytest` tests.
5. **Serves** the results through a `FastAPI` REST API.
6. **Shows** it in a `Streamlit` app where you can upload a file.
7. **Answers questions** in natural language: a local LLM (via Ollama) decides which analysis function to call (*function calling*) and explains the result.

## How the LLM assistant works

The LLM does not read the data directly and does not invent numbers. Instead:

```
User question  ->  LLM chooses a tool (an analysis function)
                         |
                         v
               Python function runs on the real data
                         |
                         v
               Result goes back to the LLM  ->  answer in plain language
```

Example: *"Which strain grows the fastest?"* -> the LLM calls the fastest-strain function -> the function returns the result with its units -> the LLM writes the answer.

The prompt is kept strict, and tool results include units, to reduce wrong or made-up answers.

## Tech stack

| Part | Tool |
|---|---|
| Language | Python |
| Data handling | pandas |
| Validation / schema | pydantic |
| Storage | SQLite, JSON |
| API | FastAPI |
| Web interface | Streamlit |
| Local LLM | Ollama (function calling) |
| Tests | pytest |

## Project structure

```
DataLabAssistant/
├── app/            # API and web interface
├── data/           # data storage
├── scripts/        # helper scripts (e.g. makeFakeData.py)
├── src/            # parsing, schema, analysis functions
├── tests/          # pytest tests
└── requirements.txt
```

## Getting started

### 1. Clone and install

```bash
git clone https://github.com/jeyji1949/DataLabAssistant.git
cd DataLabAssistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate fake messy data

The project uses a generated file, so no real lab data is needed:

```bash
python scripts/makeFakeData.py
```

### 3. Run the API

```bash
# TODO: check this command matches your file name
uvicorn app.main:app --reload
```

Then open <http://127.0.0.1:8000/docs> for the interactive API documentation.

Main endpoints:

| Endpoint | Description |
|---|---|
| `GET /strains` | List all strains |
| `GET /strains/{strain}/summary` | Summary statistics for one strain |
| `GET /fastest-strain` | Strain with the fastest growth |

### 4. Run the web interface

```bash
# TODO: check this command matches your file name
streamlit run app/<your_streamlit_file>.py
```

### 5. Use the LLM assistant

1. Install [Ollama](https://ollama.com) and download a model that supports tool calling:

   ```bash
   ollama pull <model-name>   # TODO: put the model you use
   ```

2. Start the assistant and ask a question, for example *"Which strain grows the fastest?"*

## Run the tests

```bash
pytest
```

## Roadmap

- [x] Messy data generator
- [x] Parsing and pydantic validation
- [x] SQLite / JSON storage
- [x] Analysis functions with pytest tests
- [x] FastAPI endpoints
- [x] Streamlit upload page
- [x] Local LLM assistant with function calling
- [ ] Docker packaging
- [ ] Evaluation of the LLM answers (a set of reference questions and expected answers)

## What I learned

- How to clean and validate real-world messy data before using it.
- How to separate parsing, analysis, API and interface into clear parts.
- How function calling lets an LLM use real tools instead of guessing.
- Why tests matter: each analysis function is checked on its own.

## Author

Jihane El Khraibi, Master's student in Bioinformatics and AI for Precision Medicine (FSDM, Fès).
[LinkedIn](https://www.linkedin.com/in/jihane-el-khraibi) · [GitHub](https://github.com/jeyji1949)
