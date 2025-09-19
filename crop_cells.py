import cv2
import numpy as np
import sys
import os

def find_non_black_pixels(image, tolerance=30):
    """
    Find the first non-black pixel from each corner along horizontal or vertical axes.
    
    Args:
        image: Input image (BGR format)
        tolerance: Tolerance for considering a pixel as black (0-255)
    
    Returns:
        dict: Dictionary with results for each corner containing:
              - 'index': index of first non-black pixel
              - 'axis': 'horizontal' or 'vertical'
    """
    height, width = image.shape[:2]
    results = {}
    
    def is_black_pixel(pixel, tolerance):
        """Check if a pixel is considered black within tolerance"""
        return np.all(pixel <= tolerance)
    
    # Top-left corner
    axis = ''
    index = 0
    for x in range(width):
        if not is_black_pixel(image[0, x], tolerance):
            index = x
            axis = 'horizontal'
            break
        if not is_black_pixel(image[x, 0], tolerance):
            index = x
            axis = 'vertical'
            break
    results['top_left'] = (index, axis)

    # Top-right corner
    for x in range(width):
        if not is_black_pixel(image[0, width-x-1], tolerance):
            index = x
            axis = 'horizontal'
            break
        if not is_black_pixel(image[x, width-1], tolerance):
            index = x
            axis = 'vertical'
            break
    results['top_right'] = (index, axis)

    # Bottom-left corner
    for x in range(width):
        if not is_black_pixel(image[height-1, x], tolerance):
            index = x
            axis = 'horizontal'
            break
        if not is_black_pixel(image[height-x-1, 0], tolerance):
            index = x
            axis = 'vertical'
            break
    results['bottom_left'] = (index, axis)
    
    # Bottom-right corner
    for x in range(width):
        if not is_black_pixel(image[height-1, width-x-1], tolerance):
            index = x
            axis = 'horizontal'
            break
        if not is_black_pixel(image[height-x-1, width-1], tolerance):
            index = x
            axis = 'vertical'
            break
    results['bottom_right'] = (index, axis)    
    
    return results

def crop_and_save(image, non_black, image_filename, crop_tolerance=5):
    """
    Crop the image based on non-black pixel positions and save the cropped image.
    
    Args:
        image: Input image (BGR format)
        non_black: Dictionary with non-black pixel positions from corners
        image_filename: Original image filename for saving cropped image
        crop_tolerance: Additional pixels to include in crop
    """
    height, width = image.shape[:2]
    
    left = 0
    right = width
    top = 0
    bottom = height
    
    # Determine left boundary
    if non_black['top_left'][1] == 'horizontal':
        left = non_black['top_left'][0] + crop_tolerance
    if non_black['bottom_left'][1] == 'horizontal':
        left = max(left, non_black['bottom_left'][0] + crop_tolerance)
    
    # Determine right boundary
    if non_black['top_right'][1] == 'horizontal':
        right = width - non_black['top_right'][0] - crop_tolerance
    if non_black['bottom_right'][1] == 'horizontal':
        right = min(right, width - non_black['bottom_right'][0] - crop_tolerance)
    
    # Determine top boundary
    if non_black['top_left'][1] == 'vertical':
        top = non_black['top_left'][0] + crop_tolerance
    if non_black['top_right'][1] == 'vertical':
        top = max(top, non_black['top_right'][0] + crop_tolerance)
    
    # Determine bottom boundary
    if non_black['bottom_left'][1] == 'vertical':
        bottom = height - non_black['bottom_left'][0] - crop_tolerance
    if non_black['bottom_right'][1] == 'vertical':
        bottom = min(bottom, height - non_black['bottom_right'][0] - crop_tolerance)
    
    print(f"\nCropping coordinates: left={left}, right={right}, top={top}, bottom={bottom}")
    
    # Crop the image
    cropped_image = image[top:bottom, left:right]
    
    # Save the cropped image
    base, ext = os.path.splitext(image_filename)
    cropped_filename = f"{base}_cropped{ext}"
    cv2.imwrite(cropped_filename, cropped_image)
    print(f"Cropped image saved as '{cropped_filename}'")

def main():
    # Check if image filename is provided as command line argument
    if len(sys.argv) != 2:
        print("Usage: python3 crop_cells.py <image_filename>")
        print("Example: python3 crop_cells.py image.jpg")
        sys.exit(1)
    
    # Get the image filename from command line argument
    image_filename = sys.argv[1]
    
    # Check if the file exists
    if not os.path.exists(image_filename):
        print(f"Error: File '{image_filename}' not found.")
        sys.exit(1)
    
    # Load the image
    image = cv2.imread(image_filename)
    
    if image is None:
        print(f"Error: Could not load image '{image_filename}'. Please check if it's a valid image file.")
        sys.exit(1)
    
    print(f"Image dimensions: {image.shape[1]}x{image.shape[0]} pixels")
    print(f"Image channels: {image.shape[2]}")
    
    # Find non-black pixels from corners
    non_black = find_non_black_pixels(image, tolerance=30)
    
    print("\nNon-black pixel detection results:")
    print(non_black)

    crop_and_save(image, non_black, image_filename, crop_tolerance=5)

if __name__ == "__main__":
    main()