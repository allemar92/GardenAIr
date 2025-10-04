from agents.create_agents import(
    create_plant_selector,
    create_synergy_agent,
    create_garden_agent,
    create_summarize_map_agent
)
from images.openai_image_client import OpenAIImageClient
# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# #TODO: add logging
# logger.info("🌱 Plant list generated: %s", plant_list)
# logger.error("❌ Failed to generate garden image: %s", e)



def run_garden_pipeline(location: str, preferences: list[str], num_people: int):
    """
    Runs the gardening pipeline
    """
    #first agents: it will suggest the plant list
    plant_selector = create_plant_selector() 
    plant_list = plant_selector.ask(
        f"""I live in {location}, and I like {', '.join(preferences)}.
            I want to make a synergistic garden. 
            Add to my preference the most useful and productive garden plants that thrive in my climate zone.
            Suggest a list of plants that do well in my area and that have nice synergies.
            Avoid any tips or advice, generate only a list of plants. Avoid any explanations or introduction."""
                                    )
    if not plant_list or plant_list.startswith("Error:"):
        raise RuntimeError("Plant selector failed to generate output")


    print("🌱 Plant list generated: ",plant_list)

    #second agent: it will suggest the synergies
    synergy_agent  =create_synergy_agent()
    plants_and_synergy = synergy_agent.ask(
    f"""Based on this list of plant: {plant_list}, provide any additional synergetic plant that thrives in this location: {location}
        Return the provided list with the addition of the new plants.
        Avoid any tips or advice, generate only a list of plants. Avoid any explanations or introduction."""
                        )
    
    if not plants_and_synergy or plants_and_synergy.startswith("Error:"):
        raise RuntimeError("Plant selector failed to generate output")
    
    print(f"🌱 Synergy step complete. Plants: {plants_and_synergy}")

    #third agent: it will provide the gardening instructions
    garden_agent = create_garden_agent()
    gardening_instruction =garden_agent.ask(
        f"""Based on this list of plant: {plants_and_synergy}, provide instructions to set the garden to take full advantage of the synergies between plants
            Provide precise instructions on which plants should be planted close to each other and on the synergies to take advantage of.
            Give the right number of plants for each species to feed a family of {num_people}"""
                    )
    if not gardening_instruction or gardening_instruction.startswith("Error:"):
        raise RuntimeError("Plant selector failed to generate output")
    
    print(f"🌱 Gardening instructions generated: {gardening_instruction}")
    #fourth agent: it will summarize the map
    summarize_map_agent = create_summarize_map_agent()
    summarized_map = summarize_map_agent.ask(
            f"""
            You are a garden layout summarizer.
            Based on the following plant list: {plants_and_synergy}
            and these gardening instructions: {gardening_instruction},
            produce a concise, structured garden map.

            Rules:
            - Output ONLY a minimal description of the layout.
            - Indicate clearly which plants should be grouped together.
            - Do NOT include advice, explanations, or extra text.
            - Use a simple format like: 
            Bed 1: carrots next to onions and lettuce.
            Bed 2: tomatoes next to basil and marigold.
            """
            )
    if not summarized_map or summarized_map.startswith("Error:"):
        raise RuntimeError("Plant selector failed to generate output")
    #generate an image of the garden
    try:
        image_client = OpenAIImageClient()
        garden_image = image_client.generate_image(f"""
            Based on this layout description:
            {summarized_map}

            Generate a minimal black-and-white outline schema, similar to diagrams in textbooks.

            Rules:
            - Draw only plants, one per species.
            - Do not add text, labels, or explanations.
            - Keep the style clean, simple, and schematic.
        """, n=1, size="1024x1024")

        if not garden_image or not garden_image.startswith("http"):
            raise ValueError("Invalid image URL returned.")

        print("🌱 Garden's map generated!")

    except Exception as e:
        print(f"❌ Failed to generate garden image: {e}")
        garden_image = None  

    
    return {
    "plant_list": plant_list,
    "plants_and_synergy": plants_and_synergy,
    "gardening_instruction": gardening_instruction,
    "summarized_map": summarized_map,
    "garden_image": garden_image
}

