import base64
import io
from PIL import Image

def convert_png_to_base64(png_file_path, compression_quality=85):
    # Open the PNG image using Pillow
    with Image.open(png_file_path) as img:
        # Convert the PNG image to RGB mode (JPEG doesn't support transparency)
        img = img.convert("RGB")

        # Create an in-memory binary stream
        img_stream = io.BytesIO()

        # Save the image as a JPEG with the specified compression quality to the stream
        # img.save(img_stream, "JPEG", quality=compression_quality)
        img.save(img_stream, "JPEG")

        # Get the binary data from the stream
        img_binary = img_stream.getvalue()

        # Encode the binary data as base64
        base64_encoded = base64.b64encode(img_binary)

        # Convert the bytes to a string (decode)
        base64_string = base64_encoded.decode("utf-8")

    return base64_string

# def convert_png_to_base64(self, file_path):
#         with open(file_path, "rb") as image_file:
#             # Read the binary data of the image file
#             image_binary = image_file.read()

#             # Encode the binary data as base64
#             base64_encoded = base64.b64encode(image_binary)

#             # Convert the bytes to a string (decode)
#             base64_string = base64_encoded.decode("utf-8")

#         return base64_string

def write_base64_to_file(base64_string, output_file_path):
    with open(output_file_path, "w") as output_file:
        output_file.write(base64_string)

# Replace "your_image.png" with the path to your PNG file
png_file_path = "./captchas/capt_20240124_104708.png"
base64_representation = convert_png_to_base64(png_file_path)

# Replace "output.txt" with the desired output file path
output_file_path = "./outputs/output-3.txt"
write_base64_to_file(base64_representation, output_file_path)