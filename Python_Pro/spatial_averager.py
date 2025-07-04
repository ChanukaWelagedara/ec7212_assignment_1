
import numpy as np
import cv2
def spatial_average(image, kernel_size):
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
    averaged = cv2.filter2D(image, -1, kernel, borderType=cv2.BORDER_REPLICATE)
    return averaged

def process_image(image_path, kernel_size):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None, "Failed to load image"
    try:
        kernel_size = int(kernel_size)
        if kernel_size <= 0:
            return None, "Kernel size must be positive"
        result = spatial_average(img, kernel_size)
        return result, None
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        image_path = sys.argv[1]
        kernel_size = int(sys.argv[2])
        result, error = process_image(image_path, kernel_size)
        if error:
            print(f"Error: {error}")
        else:
            cv2.imshow(f"{kernel_size}x{kernel_size} Spatial Average", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        print("Usage: python spatial_averager.py <image_path> <kernel_size>")
