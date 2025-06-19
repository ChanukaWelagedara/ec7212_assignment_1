import numpy as np
import cv2

def reduce_intensity_levels(image, levels):
    # Check if levels is a power of 2
    if not (levels & (levels-1) == 0) and levels != 0:
        raise ValueError("Number of levels must be a power of 2")
    # Make a copy of the image
    reduced_img = image.copy()
    # Calculate factor to divide by
    factor = 256 // levels
    # Reduce intensity levels
    reduced_img = (reduced_img // factor) * factor
    return reduced_img

def process_image(image_path, levels):
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None, "Failed to load image"
    try:
        # Convert levels to integer
        levels = int(levels)
        # Check if levels is a power of 2
        if not (levels & (levels-1) == 0) and levels != 0:
            return None, "Number of levels must be a power of 2 (2, 4, 8, 16, 32, 64, 128)"
        # Process the image
        result = reduce_intensity_levels(img, levels)
        return result, None
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        image_path = sys.argv[1]
        levels = int(sys.argv[2])
        result, error = process_image(image_path, levels)
        if error:
            print(f"Error: {error}")
        else:
            cv2.imshow(f"Reduced to {levels} levels", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        print("Usage: python intensity_reducer.py <image_path> <levels>")
