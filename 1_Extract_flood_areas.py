import os
import cv2
import numpy as np

def gen_foreground(img_folder, mask_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the image folder
    for img_name in os.listdir(img_folder):
        img_path = os.path.join(img_folder, img_name)

        # Get the filename without extension
        img_name_without_ext = os.path.splitext(img_name)[0]

        # Find the corresponding mask image (supports different extensions)
        mask_name = None
        for file in os.listdir(mask_folder):
            if os.path.splitext(file)[0] == img_name_without_ext:
                mask_name = file
                break

        if mask_name is None:
            print(f"Mask for {img_name} not found, skipping...")
            continue

        mask_path = os.path.join(mask_folder, mask_name)

        # Read the image and mask (supports multi-channel)
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)

        # Check if the image and mask are read successfully
        if img is None:
            print(f"Failed to read {img_name}, skipping...")
            continue
        if mask is None:
            print(f"Failed to read mask for {mask_name}, skipping...")
            continue

        # Ensure the mask is single-channel (convert to grayscale if not)
        if len(mask.shape) == 3:  # If the mask is multi-channel
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)  # Convert to single-channel grayscale

        # Ensure the image and mask have the same dimensions
        if img.shape[:2] != mask.shape[:2]:
            print(f"Image and mask dimensions do not match for {img_name}, skipping...")
            continue

        # Process image channels
        if len(img.shape) == 2:  # Single-channel grayscale image
            b = g = r = img  # Copy to three channels
        elif len(img.shape) == 3:  # Multi-channel image
            if img.shape[2] == 3:  # 3 channels (RGB)
                b, g, r = cv2.split(img)
            elif img.shape[2] == 4:  # 4 channels (RGBA)
                b, g, r, _ = cv2.split(img)  # Ignore Alpha channel
            else:
                print(f"Unsupported number of channels in {img_name}, skipping...")
                continue
        else:
            print(f"Unsupported image format for {img_name}, skipping...")
            continue

        # Create result image (4 channels: B, G, R, Mask)
        res = np.zeros((img.shape[0], img.shape[1], 4), dtype=img.dtype)
        res[:, :, 0] = b
        res[:, :, 1] = g
        res[:, :, 2] = r
        res[:, :, 3] = mask

        # Save the result
        output_name = f"{img_name_without_ext}.png"  # Output filename (uniformly in PNG format)
        output_path = os.path.join(output_folder, output_name)
        cv2.imwrite(output_path, res)
        print(f"Processed and saved {output_name}")

if __name__ == "__main__":
    img_folder = r".\data\origin_data\pic"    # All annotated debris flow original images
    mask_folder = r".\data\origin_data\mask"  # Corresponding mask images for annotated debris flow
    output_folder = r".\data\origin_data\pic_color"  # Save path for extracted color parts of original images

    gen_foreground(img_folder, mask_folder, output_folder)