from PIL import Image
import os
import random


def augment_image(image, mask, output_image_dir, output_mask_dir, base_filename, image_count=5,
                  rotate_range=[0, 90, 180, 270], flip_prob=0.5, scale_range=(0.8, 1.2)):
    """
    Perform data augmentation (rotation, flipping, scaling) on the input image and its corresponding mask image.
    Generate a specified number of variant images and save them to the output directories.

    Parameters:
        image (PIL.Image): Input color image
        mask (PIL.Image): Input mask image
        output_image_dir (str): Output directory for color images
        output_mask_dir (str): Output directory for mask images
        base_filename (str): Base filename (used to generate output filenames)
        image_count (int): Number of images to generate, default is 5
        rotate_range (list[int]): List of rotation angles, default is [0, 90, 180, 270]
        flip_prob (float): Probability of horizontal flipping, default is 0.5 (50% chance to flip)
        scale_range (tuple): Scaling range, default is (0.8, 1.2)

    Returns:
        None: The function directly outputs images to the specified directories
    """
    width, height = image.size

    for i in range(image_count):
        augmented_image = image.copy()
        augmented_mask = mask.copy()

        # Random rotation
        rotation_angle = random.choice(rotate_range)
        if rotation_angle != 0:
            augmented_image = augmented_image.rotate(rotation_angle, expand=True)
            augmented_mask = augmented_mask.rotate(rotation_angle, expand=True)

        # Random horizontal flip
        if random.random() < flip_prob:
            augmented_image = augmented_image.transpose(Image.FLIP_LEFT_RIGHT)
            augmented_mask = augmented_mask.transpose(Image.FLIP_LEFT_RIGHT)

        # Random scaling
        scale_factor = random.uniform(scale_range[0], scale_range[1])
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        augmented_image = augmented_image.resize((new_width, new_height), Image.LANCZOS)
        augmented_mask = augmented_mask.resize((new_width, new_height), Image.NEAREST)

        # Save image and mask with consistent filenames
        output_filename = f"{base_filename}_aug_{i + 1}"
        image_output_path = os.path.join(output_image_dir, f"{output_filename}.png")
        mask_output_path = os.path.join(output_mask_dir, f"{output_filename}.png")

        augmented_image.save(image_output_path, format="PNG")
        augmented_mask.save(mask_output_path, format="PNG")

        print(f"Generated images saved as {image_output_path} and {mask_output_path}")


def augment_images_in_folder(image_folder, mask_folder, output_dir, image_count=5, rotate_range=[0, 90, 180, 270],
                             flip_prob=0.5, scale_range=(0.8, 1.2)):
    """
    Perform data augmentation on color images and their corresponding mask images in specified folders.

    Parameters:
        image_folder (str): Path to the color image folder
        mask_folder (str): Path to the mask image folder
        output_dir (str): Output directory
        image_count (int): Number of variants to generate for each image pair, default is 5
        rotate_range (list[int]): List of rotation angles, default is [0, 90, 180, 270]
        flip_prob (float): Probability of horizontal flipping, default is 0.5 (50% chance to flip)
        scale_range (tuple): Scaling range, default is (0.8, 1.2)

    Returns:
        None: The function directly outputs images to the specified directories
    """
    os.makedirs(output_dir, exist_ok=True)
    output_image_dir = os.path.join(output_dir, "images")
    output_mask_dir = os.path.join(output_dir, "masks")
    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_mask_dir, exist_ok=True)

    image_files = os.listdir(image_folder)
    mask_files = os.listdir(mask_folder)

    for image_file in image_files:
        image_name, image_ext = os.path.splitext(image_file)
        mask_file = f"{image_name}{image_ext}"

        if mask_file in mask_files:
            image_path = os.path.join(image_folder, image_file)
            mask_path = os.path.join(mask_folder, mask_file)

            try:
                image = Image.open(image_path)
                mask = Image.open(mask_path)
            except Exception as e:
                print(f"Unable to open {image_path} or {mask_path}, error: {e}")
                continue

            augment_image(image, mask, output_image_dir, output_mask_dir, image_name, image_count, rotate_range,
                          flip_prob, scale_range)
        else:
            print(f"Warning: No corresponding mask file found for {image_file}")


# Example usage:
if __name__ == "__main__":
    image_folder = r'.\data\origin_data\pic_color'  # Path to color debris flow image folder
    mask_folder = r'.\data\origin_data\mask'  # Path to mask image folder
    output_dir = r'.\data\expand_flow_data'  # Output directory
    rotate_range = [0, 90, 270]  # Rotation angles
    flip_prob = 0.3  # 30% probability of horizontal flipping
    scale_range = (0.85, 1.15)  # Scaling range

    augment_images_in_folder(image_folder, mask_folder, output_dir, image_count=2, rotate_range=rotate_range,
                             flip_prob=flip_prob, scale_range=scale_range)  # image_count can be set to control the number of augmentations per dataset image