from agents.create_agents import(
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
# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# #TODO: add logging
# logger.info("🌱 Plant list generated: %s", plant_list)
# logger.error("❌ Failed to generate garden image: %s", e)



def run_garden_pipeline(location: str, preferences: list[str], num_people: int, client):
    """
    Runs the gardening pipeline

    """
    prompt_loader = PromptLoader(base_context={"name": "PlantSelector"})

    input_data = PlantSelectorInput(location=location,
                                    preferences=preferences,
                                    num_people=num_people)
    
    system_prompt = prompt_loader.render("plant_selector/plant_selector_system.j2", {})
    user_prompt = prompt_loader.render("plant_selector/plant_selector_user.j2", input_data.model_dump())

    full_prompt = f"{system_prompt}\n{user_prompt}"

    plant_selector = create_plant_selector() 
    raw_response = plant_selector.ask(full_prompt, client=client, model=plant_selector.model)

    try:
        if isinstance(raw_response, PlantSelectorOutput):
            plant_list = raw_response
        elif isinstance(raw_response, str):
            plant_list = parse_agent_output(raw_response, PlantSelectorOutput)
        else:
            plant_list = PlantSelectorOutput(**raw_response)
        print(f"🌱 Plant list generated: {plant_list.plant_list}") 

    except ValueError as e:
        print(f"Plant selection failed: {e}")
        raise RuntimeError("Plant selector failed to generate valid output")


    prompt_loader = PromptLoader(base_context={"name": "SynergyAgent"})

    input_data = SynergyAgentInput(plant_list=plant_list.plant_list, location=location)

    system_prompt = prompt_loader.render("synergy_agent/synergy_agent_system.j2", {})
    user_prompt = prompt_loader.render("synergy_agent/synergy_agent_user.j2", input_data.model_dump())

    full_prompt = f"{system_prompt}\n{user_prompt}"

    synergy_agent  = create_synergy_agent()

    raw_response = synergy_agent.ask(full_prompt, client=client, model=synergy_agent.model)

    try:
        if isinstance(raw_response, SynergyAgentOutput):
            plants_and_synergy = raw_response
        elif isinstance(raw_response, str):
            plants_and_synergy = parse_agent_output(raw_response, SynergyAgentOutput)
        else:
            plants_and_synergy = SynergyAgentOutput(**raw_response)

        print(f"🌱 Synergy step complete. Plants: {plants_and_synergy.plants_and_synergy}")

    except ValueError as e:
        print(f"Synergy step failed: {e}")
        raise RuntimeError("Synergy agent failed to generate valid output")


    prompt_loader = PromptLoader(base_context={"name": "GardenAgent"})

    input_data = GardenAgentInput(plants_and_synergy=plants_and_synergy.plants_and_synergy, num_people=num_people)

    system_prompt = prompt_loader.render("garden_agent/garden_agent_system.j2", {})
    user_prompt = prompt_loader.render("garden_agent/garden_agent_user.j2", input_data.model_dump())

    full_prompt = f"{system_prompt}\n{user_prompt}"

    garden_agent = create_garden_agent()
    raw_response = garden_agent.ask(full_prompt, client=client, model=garden_agent.model)

    try:
        if isinstance(raw_response, GardenAgentOutput):
            gardening_instruction = raw_response
        elif isinstance(raw_response, str):
            gardening_instruction = parse_agent_output(raw_response, GardenAgentOutput)
        else:
            gardening_instruction = GardenAgentOutput(**raw_response)

        print(f"🌱 Gardening instructions generated: {gardening_instruction.gardening_instruction}")

    except ValueError as e:
        print(f"Garden agent step failed: {e}")
        raise RuntimeError("Garden agent failed to generate valid output")
    
    prompt_loader = PromptLoader(base_context={"name": "SummarizeMapAgent"})

    input_data = SummarizeMapAgentInput(plants_and_synergy=plants_and_synergy.plants_and_synergy, gardening_instruction=gardening_instruction.gardening_instruction)

    system_prompt = prompt_loader.render("summarize_map_agent/summarize_map_system.j2", {})
    user_prompt = prompt_loader.render("summarize_map_agent/summarize_map_user.j2", input_data.model_dump())

    full_prompt = f"{system_prompt}\n{user_prompt}"

    summarize_map_agent = create_summarize_map_agent()
    raw_response = summarize_map_agent.ask(full_prompt, client=client, model=summarize_map_agent.model)

    try:
        if isinstance(raw_response, SummarizeMapAgentOutput):
            summarized_map = raw_response
        elif isinstance(raw_response, str):
            summarized_map = parse_agent_output(raw_response, SummarizeMapAgentOutput)
        else:
            summarized_map = SummarizeMapAgentOutput(**raw_response)

        print(f"🌱 Gardening's layout summarized: {summarized_map.summarized_map}")

    except ValueError as e:
        print(f"Map summarization step failed: {e}")
        raise RuntimeError("Map summarizer agent failed to generate valid output")

    #generate an image of the garden
    try:
        image_client = OpenAIImageClient()
        garden_image = image_client.generate_image(f"""
            Based on this layout description:
            {summarized_map.summarized_map}

            Generate a minimal black-and-white outline schema, similar to diagrams in textbooks.

            Rules:
            - Draw only plants, one per species.
            - Do not add text, labels, or explanations.
            - Keep the style clean, simple, and schematic.
        """,  size="1024x1024")

        print("DEBUG - garden_image response:", garden_image)

        if not garden_image or not garden_image.startswith("http"):
            raise ValueError("Invalid image URL returned.")

        print("🌱 Garden's map generated!")

    except Exception as e:
        print(f"❌ Failed to generate garden image: {e}")
        garden_image = None  

    return {
        "plant_list": plant_list.plant_list,
        "plants_and_synergy": plants_and_synergy.plants_and_synergy,
        "gardening_instruction": gardening_instruction.gardening_instruction,
        "summarized_map": summarized_map.summarized_map,
        "garden_image": garden_image
    }

