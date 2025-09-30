from agents.create_agents import(
    create_plant_selector,
    create_synergy_agent,
    create_garden_agent,
    create_summarize_map_agent
)
from images.openai_image_client import OpenAIImageClient

def run_garden_pipeline(location: str, preferences: list[str], num_people: int):
    """
    Runs the gardening pipeline
    """
    #first agents: it will suggest the plant list
    plant_selector = create_plant_selector() 
    plant_list = plant_selector.ask(
        f"I live in {location}, and I like {', '.join(preferences)}."
        "I want to make a synergistic garden. "
        "Add to my preference the most useful and productive garden plants that thrive in my climate zone."
        "Suggest a list of plants that do well in my area and that have nice synergies."
        "Avoid any tips or advice, generate only a list of plants. Avoid any explanations or introduction."
                                    )
    
    #second agent: it will suggest the synergies
    synergy_agent  =create_synergy_agent()
    plants_and_synergy = synergy_agent.ask(
    f"Based on this list of plant: {plant_list}, provide any additional synergetic plant that thrives in this location: {location}"
    "Return the provided list with the addition of the new plants."
    "Avoid any tips or advice, generate only a list of plants. Avoid any explanations or introduction."
                        )

    #third agent: it will provide the gardening instructions
    garden_agent = create_garden_agent()
    gardening_instruction =garden_agent.ask(
        f"Based on this list of plant: {plants_and_synergy}, provide instructions to set the garden to take full advantage of the synergies between plants"
        "Provide precise instructions on which plants should be planted close to each other and on the synergies to take advantage of."
        "Give the right number of plants for each species to feed a family of {num_people}"
                    )
    
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
    
    #generate an image of the garden
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
    
    return gardening_instruction,garden_image
