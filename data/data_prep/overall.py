from pathlib import Path
from vid2image import ProcessAllHSV,FrameCapture
from un2cropped import process_images,resize_images_to_60x60

if __name__ == '__main__':
    # Set the input folder containing the video files
    img_path = Path().cwd().parent / "Img"
    vid_path = Path().cwd().parent / "Vid" 
    # Call the function to process all .hsv files in the input folder
    ProcessAllHSV(vid_path, img_path / "Uncropped")

    # Process all images in the input directory
    process_images(img_path / "Uncropped", img_path / "Cropped")  # Adjust file extension if necessary
    resize_images_to_60x60(img_path / "Cropped", img_path / "Resized")  # Adjust file extension if necessary
    