from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2

def extract_frames_from_gif(gif_path):
    """
    Extracts pixel values from each frame of a GIF image.

    Parameters:
    - gif_path (str): Path to the GIF file.

    Returns:
    - frames (list): List of frames, where each frame is a 3D array [X][Y][RGBA].
    """
    print("Extracting frames from GIF...")
    frames = []
    gif = Image.open(gif_path)

    try:
        while True:
            # Extract pixel data for the current frame
            frame = gif.convert('RGBA')
            frame_pixels = list(frame.getdata())

            # Convert the flat list of pixels into a 2D list [X][Y][RGBA]
            width, height = frame.size
            frame_pixels = [frame_pixels[i * width:(i + 1) * width] for i in range(height)]

            # Append the frame to the frames list
            frames.append(frame_pixels)

            # Move to the next frame
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    print("Finished extracting frames.")
    return frames

def display_frame(frame):
    """
    Displays a single frame using matplotlib.

    Parameters:
    - frame (list): The frame to display, a 2D list of pixel values [X][Y][RGBA].
    """
    frame = np.array(frame, dtype=np.uint8)
    frame_img = Image.fromarray(frame, mode='RGBA').convert('RGB')
    plt.imshow(frame_img)
    plt.axis('off')
    plt.style.use('dark_background')
    plt.show()

def crop_frames(frames, x, y, width, height):
    """
    Crops all frames in a GIF to a new shape defined by input parameters.

    Parameters:
    - frames (list): List of frames, where each frame is a 3D array [X][Y][RGBA].
    - x (int): X-coordinate of the upper left corner of the crop area.
    - y (int): Y-coordinate of the upper left corner of the crop area.
    - width (int): Width of the crop area.
    - height (int): Height of the crop area.

    Returns:
    - cropped_frames (list): List of cropped frames, where each frame is a 3D array [X][Y][RGBA].
    """
    print("Cropping frames...")
    cropped_frames = []

    for frame in frames:
        frame_img = Image.fromarray(np.uint8(frame), mode='RGBA')
        cropped_frame_img = frame_img.crop((x, y, x + width, y + height))
        cropped_frame_np = np.array(cropped_frame_img)
        cropped_frames.append(cropped_frame_np)

    print("Finished cropping frames.")
    return cropped_frames

def replace_colors(frames, color1, color2):
    """
    Replaces specific colors in all frames of a GIF.

    Parameters:
    - frames (list): List of frames, where each frame is a 3D array [X][Y][RGBA].
    - color1 (tuple): RGB or RGBA tuple for the first replacement color.
    - color2 (tuple): RGB or RGBA tuple for the second replacement color.

    Returns:
    - modified_frames (list): List of modified frames, where each frame is a 3D array [X][Y][RGBA].
    """
    print("Replacing colors in frames...")
    modified_frames = []

    for frame in frames:
        modified_frame = []
        row = 0

        for pixel_row in frame:
            modified_row = []
            for pixel in pixel_row:
                if row < 133:
                    if pixel[2] > 210:
                        modified_pixel = color1 + pixel[len(color1):]
                    else:
                        modified_pixel = color2
                else:
                    if pixel[1] > 170:
                        modified_pixel = color1 + pixel[len(color1):]
                    else:
                        modified_pixel = color2
                modified_row.append(modified_pixel)
            row += 1
            modified_frame.append(modified_row)
        
        modified_frames.append(modified_frame)

    print("Finished replacing colors.")
    return modified_frames

def antialias_frames(frames):
    """
    Applies antialiasing to each frame in a list of frames.

    Parameters:
    - frames (list): List of frames, where each frame is a 3D array [X][Y][RGBA].

    Returns:
    - antialiased_frames (list): List of antialiased frames, where each frame is a 3D array [X][Y][RGBA].
    """
    print("Applying antialiasing to frames...")
    width, height = frames[0].shape[:2]
    antialiased_frames = []
    upscale_factor = 5

    for i, frame in enumerate(frames, start=1):
        print(f"Processing frame {i} of {len(frames)}")
        interpolated_frame = cv2.resize(frame, (height * upscale_factor, width * upscale_factor), interpolation=cv2.INTER_CUBIC)
        filtered_frame = cv2.GaussianBlur(interpolated_frame, (upscale_factor, upscale_factor), 0)
        antialiased_frame = cv2.resize(filtered_frame, (height, width), interpolation=cv2.INTER_AREA)
        antialiased_frame = cv2.GaussianBlur(antialiased_frame, (3, 3), 0)
        antialiased_frames.append(antialiased_frame)

    print("Finished applying antialiasing.")
    return antialiased_frames


def create_gif(frames, output_path):
    """
    Creates a GIF file from frames.

    Parameters:
    - frames (list): List of frames, where each frame is a PIL Image object.
    - output_path (str): Path to save the output GIF file.
    """
    print(f"Creating GIF at '{output_path}'...")
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=1000/30, loop=0)
    print("Finished creating GIF.")





if __name__ == "__main__":
    gif_path = 'input.gif'
    print(f"Loading GIF from '{gif_path}'...")
    frames = extract_frames_from_gif(gif_path)

    print(f"Number of frames: {len(frames)}")
    print(f"Dimensions of the first frame: {len(frames[0])}x{len(frames[0][0])} pixels")

    replacement_color1 = (255, 201, 111, 255)
    replacement_color2 = (0, 0, 0, 255)
    colored_frames = replace_colors(frames, replacement_color1, replacement_color2)

    x, y, width, height = 110, 60, 180, 150
    cropped_frames = crop_frames(colored_frames, x, y, width, height)

    print(f"Number of frames after cropping: {len(cropped_frames)}")
    print(f"Dimensions of the first cropped frame: {len(cropped_frames[0])}x{len(cropped_frames[0][0])} pixels")

    antialiased_frames = antialias_frames(cropped_frames)
    processed_frames = [Image.fromarray(frame) for frame in antialiased_frames][14:]

    create_gif(processed_frames, 'output.gif')
