# 🌱 GardenAIr

**AI-powered garden planning assistant that helps you design synergistic vegetable gardens tailored to your location and preferences.**

GardenAIr uses multiple AI agents to:
- 🌿 Suggest optimal plants for your climate zone
- 🤝 Identify companion planting synergies
- 📋 Generate detailed gardening instructions
- 🗺️ Create visual garden layout maps

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (optional, for containerized deployment)
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/allemar92/GardenAIr.git
   cd GardenAIr
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

   Example `.env`:
   ```
   OPENAI_API_KEY=your_api_key_here
   LITELLM_MODEL='gpt-4o-mini'
   ```

---

## 💻 Usage

### Command Line Interface (CLI)

Run the garden planning pipeline directly from the command line:

```bash
python src/main.py "Toscana" -p tomatoes -p basil -p lettuce -n 4
```

**Parameters:**
- `location`: Your climate zone or location (e.g., "Toscana", "California", "Zone 7")
- `-p, --preferences`: Plant preferences (can specify multiple)
- `-n, --num-people`: Number of people to feed (default: 4)



### API Server

Run the FastAPI backend server:

```bash
uvicorn src.api.main_api:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs


**Example API request:**
```bash
curl -X POST "http://localhost:8000/garden/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Toscana",
    "preferences": ["tomatoes", "basil", "lettuce"],
    "num_people": 4
  }'
```


## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

Run the entire application stack (backend + frontend):

```bash
docker compose up
```

This starts:
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:7860

To run in detached mode:
```bash
docker compose up -d
```

To stop:
```bash
docker compose down
```

### Customizing Prompts

Prompts are stored as Jinja2 templates in `src/prompts/`. To customize:

1. Navigate to the relevant agent folder (e.g., `src/prompts/plant_selector/`)
2. Edit the system or user prompt template
3. Use Jinja2 syntax for dynamic content: `{{ variable_name }}`

**Example:**
```jinja2
Location: {{ location }}
Preferences: {{ preferences | join(", ") }}

Generate a plant list suitable for {{ num_people }} people.
```

---

## 📊 Pipeline Architecture

GardenAIr uses a multi-agent pipeline with Pydantic validation:

```
┌─────────────────┐
│ PlantSelector   │  Suggests initial plants based on location/preferences
└────────┬────────┘
         │ validates: PlantSelectorOutput
         ▼
┌─────────────────┐
│ SynergyAgent    │  Adds companion plants for optimal synergies
└────────┬────────┘
         │ validates: SynergyAgentOutput
         ▼
┌─────────────────┐
│ GardenAgent     │  Generates detailed planting instructions
└────────┬────────┘
         │ validates: GardenAgentOutput
         ▼
┌─────────────────┐
│ SummarizeMap    │  Creates concise layout summary
└────────┬────────┘
         │ validates: SummarizeMapAgentOutput
         ▼
┌─────────────────┐
│ ImageGenerator  │  Generates visual garden map (optional)
└─────────────────┘
```

---


**Happy Gardening! 🌻**


