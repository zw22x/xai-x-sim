# uses grok to simulate what-if scenarios
import os
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from xai_sdk import Client
from xai_sdk.chat import user, system
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

load_dotenv()
console = Console()

app = typer.Typer(help="Grok-powered What-if simulator")

client = Client(api_key=os.getenv("XAI_API_KEY") or "")

SYSTEM_BASE = """
You are a maximally truth-seeking, first-principles world simulator.
Given a historical, physical, technological or social "What if" scenario,
simulate realistic causal consequences step by step.

Rules:
- Number each major step (1., 2., ...)
- Show clear cause → effect reasoning
- Stay grounded in real physics, history, incentives, human behavior
- Include short-term (years), medium-term (decades), long-term (centuries) effects when relevant
- Be detailed but concise — aim for clarity over fluff
- Add a touch of dry wit or irony only when it naturally fits
"""

def run_simulation(messages, model: str, max_tokens: int = 2200) -> str:
    with console.status("[bold green]Grok is rewriting reality..."):
        chat_session = client.chat.create(
            model=model,
            messages=messages,
            temperature=0.68,
            max_tokens=max_tokens,
        )
        completion = chat_session.sample()  # Generate the response
    return completion.content.strip()
    
@app.command()
def simulate(
    scenario: str = typer.Argument(..., help="The what-if question"),
    steps: int = typer.Option(8, "--steps", "-s", help="Target number of steps"),
    model: str = typer.Option("grok-4-0709", "--model", help="Grok model to use"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Allow mid-simulation changes"),
    output_dir: str = typer.Option("simulations", "--out", help="Folder to save results"),
):
    console.rule(f"What-if Simulator - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    console.print(Panel.fit(f"[bold]{scenario}[/bold]", title="Scenario", border_style="cyan"))

    messages = [
        system(SYSTEM_BASE + f"\nSimulate approximately {steps} causal steps."),
        user(scenario),
    ]

    full_output = f"Scenario: {scenario}\n\n"

    while True:
        result = run_simulation(messages, model)
        console.print("\n[bold cyan]Simulation:[/bold cyan]")
        console.print(result)

        full_output += f"\n{'-'*80}\n{result}\n"

        if not interactive or not Confirm.ask("\nWant to alter the timeline / ask a follow up?", default=False):
            break

        tweak = Prompt.ask("What change or question do you have? (or press Enter to finish)")
        if not tweak.strip():
            break

        messages.append(user(tweak))
        console.print(f"\n[italic dim] Continuing simulation with your adjustment... [/italic dim]")

    # save to file
    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c for c in scenario[:40] if c.isalnum() or c in " -_").strip()
    filename = out_path / f"sim_{timestamp}_{safe_name}.txt"
    filename.write_text(full_output)
    console.print(f"\n[green]Saved to:[/green] {filename}")

if __name__ == "__main__":
    app()