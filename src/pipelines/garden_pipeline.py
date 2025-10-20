from utils.logging_config import setup_logger
from agents.create_agents import (
    create_plant_selector,
    create_synergy_agent,
    create_garden_agent,
    create_summarize_map_agent
)
from data_models.plant_selector_model import PlantSelectorInput, PlantSelectorOutput
from data_models.synergy_agent_model import SynergyAgentInput, SynergyAgentOutput
from data_models.garden_agent_model import GardenAgentInput, GardenAgentOutput
from data_models.map_summarizer_model import SummarizeMapAgentInput, SummarizeMapAgentOutput
from utils.prompt_loader import PromptLoader
from utils.parse_agent_output import parse_agent_output
from images.openai_image_client import OpenAIImageClient


logger = setup_logger("garden_pipeline")

def run_garden_pipeline(location: str, preferences: list[str], num_people: int, client):
    """
    Runs the full gardening pipeline
    """
    logger.info("Starting GardenAIr pipeline for location=%s | preferences=%s | people=%d",
                location, preferences, num_people)

    # STEP 1: PLANT SELECTOR
    try:
        logger.info("🌱 Step 1: Running Plant Selector Agent")

        prompt_loader = PromptLoader(base_context={"name": "PlantSelector"})
        input_data = PlantSelectorInput(location=location, preferences=preferences, num_people=num_people)

        system_prompt = prompt_loader.render("plant_selector/plant_selector_system.j2", {})
        user_prompt = prompt_loader.render("plant_selector/plant_selector_user.j2", input_data.model_dump())
        full_prompt = f"{system_prompt}\n{user_prompt}"

        plant_selector = create_plant_selector()
        raw_response = plant_selector.ask(full_prompt, client=client, model=plant_selector.model)

        plant_list = parse_agent_output(raw_response, PlantSelectorOutput)
        logger.info("Plant selection complete — %d plants found", len(plant_list.plant_list))

    except Exception as e:
        logger.error("❌ Plant selection failed: %s", e, exc_info=True)
        raise RuntimeError("Plant selector failed to generate valid output")

    # STEP 2: SYNERGY AGENT
    try:
        logger.info("🌿 Step 2: Running Synergy Agent")

        prompt_loader = PromptLoader(base_context={"name": "SynergyAgent"})
        input_data = SynergyAgentInput(plant_list=plant_list.plant_list, location=location)

        system_prompt = prompt_loader.render("synergy_agent/synergy_agent_system.j2", {})
        user_prompt = prompt_loader.render("synergy_agent/synergy_agent_user.j2", input_data.model_dump())
        full_prompt = f"{system_prompt}\n{user_prompt}"

        synergy_agent = create_synergy_agent()
        raw_response = synergy_agent.ask(full_prompt, client=client, model=synergy_agent.model)

        plants_and_synergy = parse_agent_output(raw_response, SynergyAgentOutput)
        logger.info("Synergy step complete — %d synergies found", len(plants_and_synergy.plants_and_synergy))

    except Exception as e:
        logger.error("❌ Synergy agent failed: %s", e, exc_info=True)
        raise RuntimeError("Synergy agent failed to generate valid output")

    # STEP 3: GARDEN AGENT
    try:
        logger.info("🌻 Step 3: Running Garden Agent")

        prompt_loader = PromptLoader(base_context={"name": "GardenAgent"})
        input_data = GardenAgentInput(plants_and_synergy=plants_and_synergy.plants_and_synergy,
                                      num_people=num_people)

        system_prompt = prompt_loader.render("garden_agent/garden_agent_system.j2", {})
        user_prompt = prompt_loader.render("garden_agent/garden_agent_user.j2", input_data.model_dump())
        full_prompt = f"{system_prompt}\n{user_prompt}"

        garden_agent = create_garden_agent()
        raw_response = garden_agent.ask(full_prompt, client=client, model=garden_agent.model)

        gardening_instruction = parse_agent_output(raw_response, GardenAgentOutput)
        logger.info("Gardening instructions generated successfully")

    except Exception as e:
        logger.error("❌ Garden agent failed: %s", e, exc_info=True)
        raise RuntimeError("Garden agent failed to generate valid output")

    # STEP 4: MAP SUMMARIZER
    try:
        logger.info("🗺️ Step 4: Running Map Summarizer Agent")

        prompt_loader = PromptLoader(base_context={"name": "SummarizeMapAgent"})
        input_data = SummarizeMapAgentInput(
            plants_and_synergy=plants_and_synergy.plants_and_synergy,
            gardening_instruction=gardening_instruction.gardening_instruction
        )

        system_prompt = prompt_loader.render("summarize_map_agent/summarize_map_system.j2", {})
        user_prompt = prompt_loader.render("summarize_map_agent/summarize_map_user.j2", input_data.model_dump())
        full_prompt = f"{system_prompt}\n{user_prompt}"

        summarize_map_agent = create_summarize_map_agent()
        raw_response = summarize_map_agent.ask(full_prompt, client=client, model=summarize_map_agent.model)

        summarized_map = parse_agent_output(raw_response, SummarizeMapAgentOutput)
        logger.info("Map summarization complete")

    except Exception as e:
        logger.error("❌ Map summarization failed: %s", e, exc_info=True)
        raise RuntimeError("Map summarizer agent failed to generate valid output")

    # STEP 5: IMAGE GENERATION
    try:
        logger.info("🖼️ Step 5: Generating garden image")

        image_client = OpenAIImageClient()
        garden_image = image_client.generate_image(f"""
            Based on this layout description:
            {summarized_map.summarized_map}

            Generate a minimal black-and-white outline schema, similar to diagrams in textbooks.
        """, size="1024x1024")

        if not garden_image or not garden_image.startswith("http"):
            raise ValueError("Invalid image URL returned.")

        logger.info("Garden image generated successfully")

    except Exception as e:
        logger.warning("⚠️ Failed to generate garden image: %s", e, exc_info=True)
        garden_image = None

    # FINAL RESULT
    result = {
        "plant_list": plant_list.plant_list,
        "plants_and_synergy": plants_and_synergy.plants_and_synergy,
        "gardening_instruction": gardening_instruction.gardening_instruction,
        "summarized_map": summarized_map.summarized_map,
        "garden_image": garden_image
    }

    logger.info("🎉 Pipeline completed successfully for %s", location)
    return result