
import numpy as np
import cv2
def block_average_full(image, block_size):
    height, width = image.shape
    output = image.copy()
    for i in range(0, height - block_size + 1, block_size):
        for j in range(0, width - block_size + 1, block_size):
            block = image[i:i+block_size, j:j+block_size]
            avg = np.mean(block, dtype=np.float32)
            output[i:i+block_size, j:j+block_size] = avg
    return output.astype(np.uint8)
def process_image(image_path, block_size):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None, "Failed to load image"
    try:
        block_size = int(block_size)
        if block_size <= 0:
            return None, "Block size must be positive"
        result = block_average_full(img, block_size)
        return result, None
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
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
