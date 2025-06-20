import numpy as np
import cv2

# def reduce_intensity_levels(image, levels):
#     if not (levels & (levels-1) == 0) and levels != 0:
#         raise ValueError("Number of levels must be a power of 2")
#     reduced_img = image.copy()
#     factor = 256 // levels
#     reduced_img = (reduced_img // factor) * factor
#     return reduced_img

def reduce_intensity_levels(image, levels):
    # Convert to grayscale if not already
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    factor = 256 / levels
    reduced = np.floor(gray / factor)
    reduced = np.uint8(reduced * factor)
    return reduced


def process_image(image_path, levels):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None, "Failed to load image"
    try:
        levels = int(levels)
        if not (levels & (levels-1) == 0) and levels != 0:
            return None, "Number of levels must be a power of 2 (2, 4, 8, 16, 32, 64, 128)"
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
