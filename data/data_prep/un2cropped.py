import cv2
import numpy as np
from pathlib import Path

def detect_white_ball(image_path):
    """Detect and crop the white ball in the image using thresholding and contour detection, draw debug info on the image."""
    # Read the image
    image = cv2.imread(str(image_path))  # Convert Path to string for OpenCV compatibility
    if image is None:
        print(f"Error reading {image_path}, skipping.")
        return None, None, None

    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to remove noise
    blurred_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)

    # Apply a binary threshold to the image
    _, binary_image = cv2.threshold(blurred_image, 50, 100, cv2.THRESH_BINARY)

    # Find contours on the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour (most likely the ball)
        max_contour = max(contours, key=cv2.contourArea)

        # Enclose the contour in a circle
        ((x, y), radius) = cv2.minEnclosingCircle(max_contour)
        center = (int(x), int(y))

        if radius > 10:  # Ensure the detected object is large enough to be the ball
            # Draw the circle and center point on the original image for debugging
            debug_image = image.copy()  # Create a copy to draw the debug info

            # Draw the enclosing circle (circumference of the ball)
            cv2.circle(debug_image, center, int(radius), (0, 255, 0), 2)  # Green circle with thickness of 2

            # Draw the center point of the ball
            cv2.circle(debug_image, center, 5, (0, 0, 255), -1)  # Red point with thickness of -1 (filled)

            # Calculate crop coordinates
            r = int(radius)
            x_min = max(0, center[0] - r)
            x_max = min(image.shape[1], center[0] + r)
            y_min = max(0, center[1] - r)
            y_max = min(image.shape[0], center[1] + r)
            cropped_image = image[y_min:y_max, x_min:x_max]

            return cropped_image, center, debug_image  # Return cropped image, center coordinates, and debug image
        else:
            print(f"Ball detected in {image_path.name} is too small.")
    else:
        print(f"No white ball detected in {image_path.name}.")

    return None, None, None

def process_images(input_dir, output_dir, frame_rate=300, file_extension="*.png"):
    """Process each image in the input directory and save the cropped image with filenames based on time in nanoseconds."""
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Calculate the nanoseconds per frame based on the frame rate
    nanoseconds_per_frame = int(1e9 / frame_rate)

    # Iterate through each image in the input directory
    for frame_number, image_file in enumerate(input_dir.glob(file_extension)):
        print(f"Processing {image_file.name}...", end='\r')

        # Detect and crop the white ball
        cropped_image, center, debug_image = detect_white_ball(image_file)

        # If ball detected, save the cropped image and debug image
        if cropped_image is not None:
            # Calculate the timestamp for the current frame in nanoseconds
            timestamp_ns = frame_number * nanoseconds_per_frame

            # Create filenames based on the timestamp
            output_filename = output_dir / f"{timestamp_ns}.png"
            # debug_filename = output_dir / f"{timestamp_ns}_dbg.png"

            # Save the cropped image and the debug image
            cv2.imwrite(str(output_filename), cropped_image)
            # cv2.imwrite(str(debug_filename), debug_image)

            print(f"Saved cropped image as {output_filename.name}", end='\r')
        else:
            print(f"Skipping {image_file.name}, no valid ball found.")

def resize_images_to_60x60(input_dir, output_dir, file_extension="*.png"):
    """Resize all images in the input directory to 60x60 pixels and save them in the output directory."""
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Iterate through each image in the input directory
    for image_file in input_dir.glob(file_extension):
        print(f"Processing {image_file.name}...", end='\r')

        # Read the image
        image = cv2.imread(str(image_file))
        if image is None:
            print(f"Error reading {image_file.name}, skipping.")
            continue

        # Resize the image to 60x60 pixels
        resized_image = cv2.resize(image, (60, 60), interpolation=cv2.INTER_AREA)

        # Create the output file path
        output_filename = output_dir / image_file.name

        # Save the resized image
        cv2.imwrite(str(output_filename), resized_image)

        print(f"Saved resized image as {output_filename.name}", end='\r')

if __name__ == '__main__':
    img_path = Path().cwd() / "data"/ "Img"
    # Process all images in the input directory
    process_images(img_path / "Uncropped", img_path / "Cropped",frame_rate=300) 
    resize_images_to_60x60(img_path / "Cropped", img_path / "Resized")  # Adjust file extension if necessary




