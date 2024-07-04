# GIF_recolor
This script processes a GIF by extracting frames, recoloring pixels, cropping, applying antialiasing, and then creating a new GIF from the modified frames.


# GIF Recolor Frame Processor

This repository contains a Python script for processing GIF images, including frame extraction, color replacement, cropping, antialiasing, and GIF creation.

## Requirements

- Python 3.x
- Pillow
- numpy
- matplotlib
- opencv-python

## Usage

1. Place your input GIF file in the repository directory as `input.gif`.
2. Run the script:
   ```sh
   python gif_recolor_frame_processor.py
   ```
3. The processed GIF will be saved as `output.gif` in the same directory.

## Functions

### `extract_frames_from_gif(gif_path)`

Extracts frames from a GIF image.

### `display_frame(frame)`

Displays a single frame using matplotlib.

### `crop_frames(frames, x, y, width, height)`

Crops frames in a GIF to a specified area.

### `replace_colors(frames, color1, color2)`

Replaces colors in all frames of a GIF.

### `antialias_frames(frames)`

Applies antialiasing to frames in a GIF.

### `create_gif(frames, output_path)`

Creates a new GIF from processed frames.

## Example

```python
if __name__ == "__main__":
    gif_path = 'input.gif'
    frames = extract_frames_from_gif(gif_path)

    replacement_color1 = (255, 201, 111, 255)
    replacement_color2 = (0, 0, 0, 255)
    colored_frames = replace_colors(frames, replacement_color1, replacement_color2)

    x, y, width, height = 110, 60, 180, 150
    cropped_frames = crop_frames(colored_frames, x, y, width, height)

    antialiased_frames = antialias_frames(cropped_frames)

    processed_frames = [Image.fromarray(frame) for frame in antialiased_frames][14:]

    create_gif(processed_frames, 'output.gif')
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.