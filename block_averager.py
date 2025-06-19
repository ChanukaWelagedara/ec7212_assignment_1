
import numpy as np
import cv2

def block_average(image, block_size):
    # Get image dimensions
    height, width = image.shape
    # Calculate the new dimensions
    new_height = height // block_size
    new_width = width // block_size
    # Create output image with reduced dimensions
    reduced_img = np.zeros((new_height, new_width), dtype=np.uint8)
    # Process each block
    for i in range(new_height):
        for j in range(new_width):
            # Extract the block
            block = image[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size]
            # Calculate the average of the block
            block_avg = np.mean(block)
            # Set the corresponding pixel in the reduced image
            reduced_img[i, j] = block_avg
    # Resize the image back to original dimensions for better visualization
    resized_img = cv2.resize(reduced_img, (width, height), interpolation=cv2.INTER_NEAREST)
    return resized_img
def process_image(image_path, block_size):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None, "Failed to load image"
    try:
        # Convert block_size to integer
        block_size = int(block_size)
        # Check if block_size is valid
        if block_size <= 0:
            return None, "Block size must be positive"
        # Process the image
        result = block_average(img, block_size)
        return result, None
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    # Example usage
    import sys
    if len(sys.argv) > 2:
        image_path = sys.argv[1]
        block_size = int(sys.argv[2])
        result, error = process_image(image_path, block_size)
        if error:
            print(f"Error: {error}")
        else:
            cv2.imshow(f"{block_size}x{block_size} Block Average", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        print("Usage: python block_averager.py <image_path> <block_size>")
