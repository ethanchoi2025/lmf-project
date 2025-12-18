import os
import argparse
import fal_client
from dotenv import load_dotenv
import requests

# Load .env file
load_dotenv()

def generate_image_variations(prompt, base_output_name):
    # API 키 확인 (FAL_KEY)
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("Error: FAL_KEY environment variable not set.")
        return

    ratios = ["9:16", "1:1", "16:9"]
    
    for ratio in ratios:
        try:
            print(f"Generating image ({ratio}) using fal.ai/nano-banana-pro...")
            
            handler = fal_client.submit(
                "fal-ai/nano-banana-pro",
                arguments={
                    "prompt": prompt,
                    "aspect_ratio": ratio
                },
            )
            
            result = handler.get()
            
            if result and "images" in result and len(result["images"]) > 0:
                image_url = result["images"][0]["url"]
                print(f"Image generated ({ratio}): {image_url}")
                
                # Format filename: ad_name_9_16.png
                suffix = ratio.replace(":", "_")
                # Remove extension from base name if present
                if base_output_name.lower().endswith('.png'):
                    base_name = base_output_name[:-4]
                else:
                    base_name = base_output_name
                
                output_file = f"{base_name}_{suffix}.png"

                # Download image
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(output_file, "wb") as f:
                        f.write(response.content)
                    print(f"Success! Saved to {output_file}")
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")
            else:
                print(f"No image data found for {ratio}.")

        except Exception as e:
            print(f"Error generating image for {ratio}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate multi-ratio images using fal.ai")
    parser.add_argument("prompt", help="The prompt for image generation")
    parser.add_argument("--output", default="generated_ad", help="Base output filename (without extension)")
    args = parser.parse_args()

    generate_image_variations(args.prompt, args.output)
