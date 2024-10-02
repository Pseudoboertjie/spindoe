import cv2
from pathlib import Path
import os

def FrameCapture(video_path, output_folder):
    # Open the video file
    vidObj = cv2.VideoCapture(video_path)

    # Get total number of frames
    total_frames = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Processing {video_path.name} with {total_frames} frames.")

    # Iterate through frames
    for count in range(total_frames):
        success, image = vidObj.read()
        if success:
            # Save frame with format 'video_name_frame_no.png'
            frame_filename = os.path.join(output_folder, f"{video_path.stem}_{count}.png")
            print(f'Converting frame {count+1} of {total_frames}', end='\r')
            cv2.imwrite(frame_filename, image)
        else:
            break

    vidObj.release()
    print(f"\nCompleted processing {video_path.name}")

def ProcessAllHSV(input_folder, output_folder):
    # Find all .hsv files in the input folder
    hsv_files = list(input_folder.glob("*.hsv"))
    
    if not hsv_files:
        print(f"No .hsv files found in {input_folder}")
        return
    
    # Process each .hsv file
    for video_file in hsv_files:
        FrameCapture(video_file, output_folder)

if __name__ == '__main__':
    img_path = Path().cwd() / "data"/ "Img"
    vid_path = Path().cwd() / "data" / "Vid" 
    # Call the function to process all .hsv files in the input folder
    ProcessAllHSV(vid_path, img_path / "Uncropped")
