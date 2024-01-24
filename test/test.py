
from PIL import Image
import base64
from io import BytesIO
import io


def convert_png_to_jpg_and_base64(png_path):
    # Open the PNG image
    with Image.open(png_path) as img:
        # Create a BytesIO object to store the JPG image
        jpg_buffer = BytesIO()

        # Convert the image to RGB before saving as JPEG
        img = img.convert("RGB")

        # Save the RGB image to the buffer in JPEG format
        img.save(jpg_buffer, format="JPEG")

        # Encode the JPG image in base64
        base64_jpg = base64.b64encode(jpg_buffer.getvalue()).decode("utf-8")

    return base64_jpg

png_image_path = "./captchas/capt_20240124_093324.png"

base64_result = convert_png_to_jpg_and_base64(png_image_path)

with open("base64-output.txt", "w") as output_file:
    output_file.write(base64_result)