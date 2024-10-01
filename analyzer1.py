import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# set your grid path, which can be the same as the grid_folder in image_grids.py
grid_path = os.getenv("GRID_PATH")



client = OpenAI(api_key=api_key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_grid_pictures(grid_path):
    grid_files = [f for f in os.listdir(grid_path) if f.endswith(('.jpg', '.png'))]
    
    batch_size = 5  # Adjust based on API limitations and your needs
    results = []

    for i in range(0, len(grid_files), batch_size):
        batch = grid_files[i:i+batch_size]
        
        messages = [
            {
                "role": "system",
                "content": "You are a video analyst. Given grid pictures representing video frames, provide a description of what happens in the video. Focus on visual themes, color palettes, character positioning, scene transitions, and symbolic elements. Respond in text, no markup."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Analyzing grid pictures {i + 1} to {min(i + batch_size, len(grid_files))} out of {len(grid_files)}."
                    }
                ] + [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(os.path.join(grid_path, filename))}",
                            "detail": "high"
                        }
                    } for filename in batch
                ]
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=4000,
            temperature=0
        )

        results.append(response.choices[0].message.content)

    return "\n\n".join(results)




try:
    analysis = analyze_grid_pictures(grid_path)
    print("Analysis complete. Results:")
    print(analysis)
except Exception as e:
    print(f"An error occurred: {str(e)}")