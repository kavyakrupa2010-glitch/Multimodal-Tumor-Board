import os
from google import genai
from PIL import Image

def analyze_pathology_image(image_path: str, prompt_override: str = None) -> str:
    """
    Uses Gemini Vision to read a pathology slide and return a text description.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable not set. Please provide it in the UI."
        
    try:
        # Initialize the new google-genai client
        client = genai.Client(api_key=api_key)
        
        # gemini-2.5-flash is excellent for multimodal vision tasks rapidly
        model_name = 'gemini-2.5-flash'
        
        instruction = prompt_override or (
            "You are an expert AI pathologist assistant. Describe the key pathological features "
            "in this slide. Highlight the cellular structures, tissue architecture, potential "
            "abnormalities (like atypia, necrosis, mitosis), and give a preliminary visual assessment."
        )
        
        # Open the image file using Pillow
        image = Image.open(image_path)
        
        # Generate content with Gemini
        response = client.models.generate_content(
            model=model_name,
            contents=[image, instruction]
        )
        
        return response.text
    except Exception as e:
        return f"Error analyzing image: {str(e)}"
