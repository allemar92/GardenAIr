import gradio as gr
from src.pipelines.garden_pipeline import run_garden_pipeline
from src.clients.litellm_client import LiteLLMClient

client = LiteLLMClient().get_client()

def generate_garden(location: str, preferences: str, num_people: int):
    try:
        prefs = [p.strip() for p in preferences.split(",") if p.strip()]
        result = run_garden_pipeline(
            location=location,
            preferences=prefs,
            num_people=int(num_people),
            client=client
        )
        text_output = (
            f"🌿 **Selected Plants:** {', '.join(result['plant_list'])}\n\n"
            f"🪴 **Synergies:** {result['plants_and_synergy']}\n\n"
            f"📋 **Instructions:** {result['gardening_instruction']}\n\n"
            f"🗺️ **Map Summary:** {result['summarized_map']}"
        )
        return text_output, result['garden_image']

    except Exception as e:
        return f"❌ Error: {str(e)}", None



with gr.Blocks(title="🌱 GardenAIr — Your Garden Assistant") as demo:
    gr.Markdown(
        """
        # 🌿 GardenAIr
        _Design your ideal garden with AI._

        Enter your **location**, your **preferred plants**, and how many **people** you want to feed.  
        GardenAIr will design a complete, synergistic garden plan 🌸
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            location = gr.Textbox(label="🌍 Location", placeholder="e.g. Tuscany")
            preferences = gr.Textbox(label="🌿 Preferences", placeholder="e.g. Tomato, basil, lettuce")
            num_people = gr.Number(label="👨‍👩‍👧 Number of people", value=2)
            run_btn = gr.Button("✨ Generate My Garden")

        with gr.Column(scale=1):
            text_output = gr.Textbox(
                label="📋 GardenAIr Results",
                lines=20,         
                show_copy_button=True
            )
            image_output = gr.Image(label="🗺️ Garden Map", height=400)

    run_btn.click(
        fn=generate_garden,
        inputs=[location, preferences, num_people],
        outputs=[text_output, image_output],
    )



if __name__ == "__main__":
    demo.launch()
