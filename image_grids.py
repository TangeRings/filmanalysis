import os
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
screenshot_folder = os.getenv("SCREENSHOT_FOLDER")
grid_folder=os.getenv("GRID_FOLDER")



def create_overlapping_grids(screenshot_folder, grid_folder, grid_size=(3, 3), overlap=0):
    # Ensure output folder exists
    if not os.path.exists(grid_folder):
        os.makedirs(grid_folder)

    # Get list of image files
    image_files = sorted([f for f in os.listdir(screenshot_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])

    # Calculate the number of images per grid and step size
    images_per_grid = grid_size[0] * grid_size[1]
    step = images_per_grid - overlap

    for start_index in range(0, len(image_files), step):
        end_index = min(start_index + images_per_grid, len(image_files))
        grid_images = image_files[start_index:end_index]

        # Open images and resize them
        images = [Image.open(os.path.join(screenshot_folder, img)) for img in grid_images]
        min_width = min(img.width for img in images)
        min_height = min(img.height for img in images)
        images = [img.resize((min_width, min_height)) for img in images]

        # Create a new image with the grid layout
        grid_width = min_width * grid_size[1]
        grid_height = min_height * grid_size[0]
        grid_image = Image.new('RGB', (grid_width, grid_height))

        # Paste images into the grid
        for i, img in enumerate(images):
            row = i // grid_size[1]
            col = i % grid_size[1]
            grid_image.paste(img, (col * min_width, row * min_height))

        # Fill any empty spots with black
        for i in range(len(images), images_per_grid):
            row = i // grid_size[1]
            col = i % grid_size[1]
            black_img = Image.new('RGB', (min_width, min_height), color='black')
            grid_image.paste(black_img, (col * min_width, row * min_height))

        # Save the grid image
        output_path = os.path.join(grid_folder, f'grid_{start_index:03d}_{end_index:03d}.png')
        grid_image.save(output_path)

    print(f"Created grid images covering all {len(image_files)} input images.")




# Set the grid size and overlap images
create_overlapping_grids(screenshot_folder, grid_folder, grid_size=(3, 3), overlap=4)