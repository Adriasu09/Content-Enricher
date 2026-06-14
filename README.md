# Content Enricher

> A Python CLI that scrapes a Wikipedia topic, enriches it with AI, translates it, and exports the result to `.txt` or `.pdf`.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-pytest-brightgreen)

Content Enricher is a terminal application that walks you through a simple, guided flow:
search a topic on Wikipedia, optionally enrich the text with an AI model, optionally
translate it into another language, and optionally save any version to a file. It was built
as a bootcamp project with a focus on clean, object-oriented design and learning the
fundamentals.

## Background

This project was created during the Factoría F5 bootcamp to practice the foundations of
Python and software design: object-oriented programming, single-responsibility classes,
dependency injection, a small exception hierarchy, and testing with `pytest` and mocks.

The architecture separates three layers that never overstep each other:

- **Services** do the detail work (HTTP, AI, translation, file export) and never print.
- **Console** (`ConsoleUI`) only reads input and prints output — it never calls APIs.
- **Orchestrator** (`App`) coordinates the console and the services but does no detail work.

External sources are accessed through a source-agnostic base class plus a specific subclass
(for example `BaseScraper` + `WikipediaScraper`), so adding a new source or a new export
format means adding a subclass, not rewriting the flow.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Configuration](#configuration)
- [Security](#security)
- [Project Structure](#project-structure)
- [Tests](#tests)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Install

This project requires [Python](https://www.python.org/) 3.10 or higher.

```sh
# 1. Clone the repository
git clone https://github.com/Adriasu09/Content-Enricher.git
cd Content-Enricher

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 3. Install the dependencies
pip install -r requirements.txt
```

## Usage

Run the application from the project root:

```sh
python main.py
```

The app then guides you through a linear flow:

1. **Topic** — enter a topic to search on Wikipedia.
2. **Language** — choose the target language for translation (`en`, `es`, `fr`, `de`, `it`, `pt`).
3. **Article** — the title and first paragraphs are fetched and shown.
4. **Enrich?** — answer `y/n`; if yes, the AI expands and improves the text.
5. **Translate?** — answer `y/n`; if yes, the content is translated into the chosen language.
6. **Save?** — answer `y/n`; if yes, pick a version (original / enriched / translated),
   a format (`txt` / `pdf`), and a file name. The file is written to the `output/` folder.

If a topic is not found, the app re-asks instead of crashing. Saved files are confirmed with
their full path on disk.

## Configuration

Configuration is read from a `.env` file at the project root. Copy the provided template and
fill in your own values:

```sh
# Windows (PowerShell):
Copy-Item .env.example .env
# macOS / Linux:
cp .env.example .env
```

| Variable         | Required | Default                          | Description                                   |
| ---------------- | -------- | -------------------------------- | --------------------------------------------- |
| `GROQ_API_KEY`   | Yes      | —                                | API key for the AI provider (Groq).           |
| `WIKIPEDIA_LANG` | No       | `en`                             | Language edition of Wikipedia to scrape.      |
| `AI_BASE_URL`    | No       | `https://api.groq.com/openai/v1` | Base URL of the OpenAI-compatible AI provider.|
| `AI_MODEL`       | No       | `llama-3.1-8b-instant`           | AI model used for enrichment.                 |

You can get a free API key at [Groq](https://console.groq.com/).

## Security

API keys are secrets and must never be committed. They are read only from the `.env` file,
which is listed in `.gitignore`. Only `.env.example` (a template with placeholder values) is
committed. If you fork or share this project, double-check that your real key never leaves
your machine.

## Project Structure

```
Content-Enricher/
├── main.py                       # entry point / composition root
├── src/
│   ├── app.py                    # App: orchestrates console <-> services
│   ├── console/console_ui.py     # ConsoleUI: all input/output
│   ├── models/article.py         # Article domain object
│   ├── config/settings.py        # loads .env configuration
│   └── services/
│       ├── scraper.py            # BaseScraper (agnostic HTTP base)
│       ├── wikipedia_scraper.py  # WikipediaScraper (Wikipedia parsing)
│       ├── ai_service.py         # AIService (AI enrichment)
│       ├── translate_service.py  # TranslateService (translation)
│       ├── export_service.py     # Exporter base + TxtExporter
│       ├── pdf_exporter.py       # PdfExporter
│       └── exceptions.py         # AppError hierarchy
└── tests/                        # pytest test suite
```

## Tests

The test suite uses `pytest`. Services that hit the network or external APIs are mocked, so
no real requests are made and no API credits are spent.

```sh
pytest                               # run the whole suite
pytest tests/test_ai_service.py      # run one file
pytest -k "translate"                # run tests matching a name
```

## Maintainers

[Adriana Suárez](https://github.com/Adriasu09)

## Contributing

This is a personal bootcamp project, so it is not actively seeking contributions. Feel free
to open an [issue](https://github.com/Adriasu09/Content-Enricher/issues) if you spot a bug or
have a question. Small pull requests are welcome.

## License

[MIT](LICENSE) © Adriana Suárez
