import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def generate_image(prompt, output_file):
    # API 키 확인
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return

    client = genai.Client(api_key=api_key)

    try:
        # User requested specific model: gemini-3-pro-image-preview (Nano Banana Pro)
        model_id = 'gemini-3-pro-image-preview'
        
        print(f"Generating image using model: {model_id}...")
        
        response = client.models.generate_content(
            model=model_id,
            contents=[prompt],
        )

        # Response handling based on Google GenAI SDK documentation
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_bytes = part.inline_data.data
                    with open(output_file, "wb") as f:
                        f.write(image_bytes)
                    print(f"Success! Image saved to {output_file}")
                    return
        
        print("No image data found in the response.")

    except Exception as e:
        print(f"Error generating image: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images using Gemini Nano Banana Pro")
    parser.add_argument("prompt", help="The prompt for image generation")
    parser.add_argument("--output", default="generated_ad.png", help="Output file path")
    args = parser.parse_args()

    generate_image(args.prompt, args.output)
