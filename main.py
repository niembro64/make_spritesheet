import os
from PIL import Image

# Directory containing the images
base_directory = "/Users/ericniemeyer/Downloads/space-shooter-game-kit/Boss-spaceship-game-sprites/PNG/Boss_01/Boss_Sprites/"
sub_directories = [
    "Attack_01",
    "Attack_02",
    "Attack_03",
    "Attack_04",
    "Idle_01",
    "Idle_02",
    "Flight",
    "Death",
]

# List to hold all generated spritesheet paths
spritesheet_paths = []

for sub_directory in sub_directories:
    print(f"Processing directory: {sub_directory}")

    image_directory = os.path.join(base_directory, sub_directory)

    # Get a list of all .png files in the directory
    image_files = [f for f in os.listdir(image_directory) if f.endswith(".png")]

    if not image_files:
        print(f"No images found in {sub_directory}. Skipping...")
        continue

    print(f"Found {len(image_files)} images in {sub_directory}. Concatenating...")

    # Initialize the concatenated image as None
    concatenated_image = None

    # Loop through all the images and concatenate them
    for index, image_file in enumerate(image_files):
        print(f"Processing image {index + 1}/{len(image_files)}: {image_file}")
        image_path = os.path.join(image_directory, image_file)
        image = Image.open(image_path).convert(
            "RGBA"
        )  # Ensure the image is in RGBA mode

        if concatenated_image is None:
            # First image, no concatenation needed
            concatenated_image = image
        else:
            # Concatenate the current image to the right of the existing concatenated image
            concatenated_width = concatenated_image.width + image.width
            concatenated_height = max(concatenated_image.height, image.height)
            new_image = Image.new(
                "RGBA", (concatenated_width, concatenated_height), (0, 0, 0, 0)
            )  # RGBA mode with transparent background

            # Paste the existing concatenated image and the new image side by side
            new_image.paste(concatenated_image, (0, 0))
            new_image.paste(
                image, (concatenated_image.width, 0), mask=image
            )  # Use mask to preserve transparency

            # Update the concatenated image
            concatenated_image = new_image

    # Save the final concatenated image
    output_filename = f"Spritesheet_{sub_directory}.png"
    output_path = os.path.join(base_directory, output_filename)
    concatenated_image.save(output_path)
    spritesheet_paths.append(output_path)

    print(f"Concatenated image saved as {output_path}\n")

# Generate the combined spritesheet from all individual spritesheets
print("Generating combined spritesheet...")

# Initialize the combined spritesheet as None
combined_spritesheet = None

# Loop through all the generated spritesheets and concatenate them
for index, spritesheet_path in enumerate(spritesheet_paths):
    print(
        f"Processing spritesheet {index + 1}/{len(spritesheet_paths)}: {spritesheet_path}"
    )
    spritesheet = Image.open(spritesheet_path).convert(
        "RGBA"
    )  # Ensure the image is in RGBA mode

    if combined_spritesheet is None:
        # First spritesheet, no concatenation needed
        combined_spritesheet = spritesheet
    else:
        # Concatenate the current spritesheet below the existing combined spritesheet
        combined_width = max(combined_spritesheet.width, spritesheet.width)
        combined_height = combined_spritesheet.height + spritesheet.height
        new_image = Image.new(
            "RGBA", (combined_width, combined_height), (0, 0, 0, 0)
        )  # RGBA mode with transparent background

        # Paste the existing combined spritesheet and the new spritesheet on top of each other
        new_image.paste(combined_spritesheet, (0, 0))
        new_image.paste(spritesheet, (0, combined_spritesheet.height), mask=spritesheet)

        # Update the combined spritesheet
        combined_spritesheet = new_image

# Save the final combined spritesheet
final_output_path = os.path.join(base_directory, "Combined_Spritesheet.png")
combined_spritesheet.save(final_output_path)

print(f"Combined spritesheet saved as {final_output_path}")
