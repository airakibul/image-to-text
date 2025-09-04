from app.config import client
import base64

def extract_text_from_image_bytes(file_bytes: bytes) -> str:
    # Encode the image to base64
    image_base64 = base64.b64encode(file_bytes).decode("utf-8")

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
