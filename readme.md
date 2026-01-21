# xai-x-sim

Simulations powered by Grok — exploring alternate histories, physics scenarios, economies, and more.

> "What if...?" but Grok runs the world model.

Current focus: Agentic "What If" simulator — input a historical/physics event + change, get step-by-step consequence narrative.

## Quick Start

1. Get your xAI API key: https://console.x.ai
2. `cp .env.example .env` and add `XAI_API_KEY=your_key`
3. `pip install -r requirements.txt`
4. `python src/simulate_what_if.py --scenario "What if the Apollo 13 oxygen tank never exploded?"`

## Structure
- `src/`               → core simulation logic
- `src/simulate_what_if.py` → main entry point
- `requirements.txt`   → xai-sdk, python-dotenv, etc.

## Roadmap
- [x] Basic single-run simulation
- [ ] Multi-turn user interaction
- [ ] Branching timelines
- [ ] Economy / market sim extension
- [ ] Web UI (Streamlit/Gradio)

Built with Grok API • MIT License