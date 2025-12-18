import os
import fal_client
from dotenv import load_dotenv
import requests
import time
import argparse

# Load .env file
load_dotenv()

# Universal Negative Prompt (Safety Net)
NEGATIVE_PROMPT = "upside down phone, impossible anatomy, distorted hands, extra fingers, missing fingers, malformed limbs, floating objects, defying gravity, blurry text, gibberish, watermark, low quality, stock photo look, awkward grip"

# Define Campaign Prompts (US Ad Expert Optimized)
CAMPAIGNS = {
    "Type_A_Efficiency": {
        "concept": "Millennial Professional / Time Saving",
        "prompt_base": (
            "A high-quality, authentic POV shot of a professional's hand holding a smartphone **upright** and **vertically** against a blurry NYC street background with yellow taxis. "
            "The hand has **5 physiologically correct fingers** with a natural, firm grip. "
            "The phone screen is clearly visible and displays a clean, white minimalist app UI with the bold black text \"Market in a Minute\" spelled correctly. "
            "Natural morning sunlight, sharp focus on the phone screen. "
            "Style: Modern lifestyle photography, authentic, credible, high status."
        )
    },
    "Type_B_MoneyHacks": {
        "concept": "Gen Z / Edutainment / UGC",
        "prompt_base": (
            "A vibrant, viral-style User Generated Content (UGC) image of a young Gen Z person (20s) looking surprised and pointing upwards. "
            "The person has **symmetrical facial features** and **anatomically correct hands**. "
            "A native social media text overlay (like an Instagram Sticker) floats above, reading \"TAX HACK 101\" in bold white text with a black background. "
            "Background: A casual, colorful home studio setting. "
            "Style: TikTok/Reels thumbnail, high energy, stopping the scroll."
        )
    },
    "Type_C_FOMO": {
        "concept": "Trader / Urgency / Signal",
        "prompt_base": (
            "A cinematic close-up of a smartphone screen in a dimly lit room, held by a hand with **natural anatomy** and **correct grip**. "
            "The screen shows a glowing green candlestick stock chart surging upwards on a dark background. "
            "A realistic, urgent notification banner overlays the top of the screen with the text \"⚠️ Don't Miss Out\" clearly legible. "
            "The green light from the screen reflects realistically on the user's thumb. "
            "Style: High-tech, financial urgency, cyberpunk vibes, 8k resolution."
        )
    }
}

RATIOS = ["9:16", "1:1", "16:9"]

def run_campaign(output_dir):
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("Error: FAL_KEY environment variable not set.")
        return

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    print("🚀 Starting US Market Ad Campaign Generation (Nano Banana Pro)...\n")
    print(f"📂 Output Directory: {output_dir}\n")

    for key, data in CAMPAIGNS.items():
        print(f"--- Processing Campaign: {key} ({data['concept']}) ---")
        
        for ratio in RATIOS:
            print(f"  > Generating {ratio} format...")
            
            # Construct final prompt with safety guidelines
            full_prompt = f"{data['prompt_base']} Aspect Ratio {ratio}. Ensure {NEGATIVE_PROMPT} are avoided."
            
            try:
                handler = fal_client.submit(
                    "fal-ai/nano-banana-pro",
                    arguments={
                        "prompt": full_prompt,
                        "aspect_ratio": ratio,
                        # negative_prompt is sometimes supported as a separate arg, 
                        # but putting it in the main prompt is safer for general models unless specified.
                        # We will try to pass it if the model supports it, or just rely on the prompt description.
                        # Nano Banana Pro is very smart, so descriptive instructions work best.
                    },
                )
                
                result = handler.get()
                
                if result and "images" in result and len(result["images"]) > 0:
                    image_url = result["images"][0]["url"]
                    
                    # Formatting filename
                    filename = f"Ad_{key}_{ratio.replace(':', '_')}.png"
                    output_path = os.path.join(output_dir, filename)
                    
                    # Download
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        with open(output_path, "wb") as f:
                            f.write(response.content)
                        print(f"    ✅ Saved: {output_path}")
                    else:
                        print(f"    ❌ Download failed for {filename}")
                else:
                    print(f"    ⚠️ No image data returned for {key} {ratio}")

            except Exception as e:
                print(f"    ❌ Error: {e}")
            
            # Small delay to respect rate limits if any
            time.sleep(1)
        print("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ad generation campaign")
    parser.add_argument("--output_dir", default="../../campaigns/h01_efficiency_na/02_assets", help="Directory to save generated images")
    args = parser.parse_args()

    # Convert relative path to absolute path based on script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # If the provided path is relative, make it relative to the script
    if not os.path.isabs(args.output_dir):
        abs_output_dir = os.path.join(script_dir, args.output_dir)
    else:
        abs_output_dir = args.output_dir

    run_campaign(abs_output_dir)

