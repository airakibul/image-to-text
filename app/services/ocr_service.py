from app.config import client
from app.utils.image_utils import encode_image_to_base64

def extract_text_from_image(image_path: str) -> str:
    image_base64 = encode_image_to_base64(image_path)

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Extract the text from this handwritten note."},
                {"type": "input_image", "image_url": f"data:image/jpeg;base64,{image_base64}"}
            ]
        }]
    )
    return response.output_text
