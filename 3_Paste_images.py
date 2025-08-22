from PIL import Image
import os
import random
import shutil

# Background images folder path
background_folder_path = r'.\data\background_data'  # Background images folder path

# Mudslide images folder path
mudslide_folder_path = r'.\data\expand_flow_data\images'  # Folder path for expanded mudslide images

# Mask images folder path
mask_folder_path = r'.\data\expand_flow_data\masks'  # Folder path for expanded mask images

# Output folder path
output_folder_path = r'.\data\finally_flow_data\images'  # Folder path to save final result images

# Output mask folder path
output_mask_folder_path = r'.\data\finally_flow_data\masks'  # Folder path to save final mask images

# Create output folders if they don't exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)
if not os.path.exists(output_mask_folder_path):
    os.makedirs(output_mask_folder_path)

# Get all background images in the folder
background_images = [f for f in os.listdir(background_folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Get all mudslide images in the folder
mudslide_images = [f for f in os.listdir(mudslide_folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Get all mask images in the folder
mask_images = [f for f in os.listdir(mask_folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Set the number of randomly selected mudslide images each time
num_random_images = 70  # User can modify this value

# Process each background image
for background_image_name in background_images:
    # Load background image
    background_image_path = os.path.join(background_folder_path, background_image_name)
    background = Image.open(background_image_path)

    # Randomly select the specified number of mudslide images
    random_mudslide_images = random.sample(mudslide_images, min(num_random_images, len(mudslide_images)))

    # Process each randomly selected mudslide image
    for mudslide_image_name in random_mudslide_images:
        # Load mudslide image
        mudslide_image_path = os.path.join(mudslide_folder_path, mudslide_image_name)
        mudslide = Image.open(mudslide_image_path)

        # Ensure mudslide image is in RGBA mode (with alpha channel)
        if mudslide.mode != 'RGBA':
            mudslide = mudslide.convert('RGBA')

        # Get dimensions of mudslide image
        mudslide_width, mudslide_height = mudslide.size

        # Resize background image to match mudslide image dimensions
        background_resized = background.resize((mudslide_width, mudslide_height), Image.Resampling.LANCZOS)

        # Create a copy of the background image to avoid modifying the original
        new_background = background_resized.copy()

        # Generate random position for mudslide image on the background
        # Assumes position is randomly within the background image bounds
        max_x = new_background.width - mudslide_width
        max_y = new_background.height - mudslide_height
        position = (random.randint(0, max_x), random.randint(0, max_y))

        # Paste mudslide image onto the background copy
        new_background.paste(mudslide, position, mudslide)

        # Generate output image name combining background and mudslide image names
        output_image_name = f"{os.path.splitext(background_image_name)[0]}_{mudslide_image_name}"
        output_image_path = os.path.join(output_folder_path, output_image_name)

        # Save result image to output folder
        new_background.save(output_image_path)

        # Copy corresponding mask image to output mask folder
        mask_image_name = mudslide_image_name  # Assuming mask image name matches mudslide image name
        mask_image_path = os.path.join(mask_folder_path, mask_image_name)
        output_mask_name = output_image_name  # Ensure mask image name matches output image name
        output_mask_path = os.path.join(output_mask_folder_path, output_mask_name)

        if os.path.exists(mask_image_path):
            shutil.copy(mask_image_path, output_mask_path)
            print(f"Copied mask image saved as {output_mask_path}")
        else:
            print(f"Warning: No corresponding mask image found for {mudslide_image_name}")

        print(f"Processed image saved as {output_image_path}")