import base64

def convert_png_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        # Read the binary data of the image file
        image_binary = image_file.read()

        # Encode the binary data as base64
        base64_encoded = base64.b64encode(image_binary)

        # Convert the bytes to a string (decode)
        base64_string = base64_encoded.decode("utf-8")

    return base64_string

def write_base64_to_file(base64_string, output_file_path):
    with open(output_file_path, "w") as output_file:
        output_file.write(base64_string)

# Replace "your_image.png" with the path to your PNG file
png_file_path = "./captchas/capt_20240123_143832.png"
base64_representation = convert_png_to_base64(png_file_path)

# Replace "output.txt" with the desired output file path
output_file_path = "output.txt"
write_base64_to_file(base64_representation, output_file_path)