
import typer
from typing import List
from clients.openai_client import OpenAIClient
from pipelines.garden_pipelines import run_garden_pipeline



app = typer.Typer(help="🌿 CLI for the Synergistic Garden Generator")

@app.command("run-garden-pipeline")
def run_garden_pipeline_cli(
    location: str = typer.Argument(..., help="Location or climate zone (es. Toscana, Firenze, Italia)"),
    preferences: List[str] = typer.Option(..., "--preference", "-p", help="List of preferred vegetables and berries (es. tomatoes, lettuce, carrots)"),
    num_people: int = typer.Option(4, "--num-people", "-n", help="Number of people to feed", min=1)
                            ):
    """
    It runs the full pipeline to generate synergistic garden.
    """

    typer.echo("🌱 Starting the Synergistic Garden pipeline")
    client: OpenAIClient = OpenAIClient().get_client()
    result = run_garden_pipeline(location, preferences, num_people, client=client)

    typer.echo("\n✅ Pipeline succesfully completed!\n")
    typer.echo("📋 Suggested plant list:")
    typer.echo(result["plant_list"])

    typer.echo("\n🌱 Plants and Synergies:")
    typer.echo(result["plants_and_synergy"])

    typer.echo("\n🌱 Gardening instructions:")
    typer.echo(result["gardening_instruction"])

    typer.echo("\n🌱 Garden Layout :")
    typer.echo(result["summarized_map"])

    if result["garden_image"]:
        typer.echo(f"\n🌱 Generated Garden map: {result['garden_image']}")
    else:
        typer.echo("\n⚠️ No generated image.")

# Entry point
if __name__ == "__main__":
    app()
