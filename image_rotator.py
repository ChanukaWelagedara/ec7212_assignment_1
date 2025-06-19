import numpy as np
import cv2

def rotate_image(image, angle):
    # Get image dimensions
    height, width = image.shape[:2]
    # Calculate the center of the image
    center = (width / 2, height / 2)
    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    # Apply the rotation
    rotated_img = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotated_img

def process_image(image_path, angle):
  
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None, "Failed to load image"
    try:
        # Convert angle to float
        angle = float(angle)
        # Process the image
        result = rotate_image(img, angle)
        return result, None
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    # Example usage
    import sys
    if len(sys.argv) > 2:
        image_path = sys.argv[1]
        angle = float(sys.argv[2])
        result, error = process_image(image_path, angle)
        if error:
            print(f"Error: {error}")
        else:
            cv2.imshow(f"Rotated by {angle} degrees", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        print("Usage: python image_rotator.py <image_path> <angle>")
