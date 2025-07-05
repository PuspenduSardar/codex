import argparse
import os
import numpy as np
from PIL import Image, ImageOps
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def preprocess_image(image_path, threshold=128, invert=True):
    """
    Converts any image to a black-and-white binary mask suitable for a word cloud.
    """
    img = Image.open(image_path).convert("L")  # Grayscale
    if invert:
        img = ImageOps.invert(img)  # Invert: shape should be white

    # Apply threshold
    binary_mask = img.point(lambda p: 255 if p > threshold else 0)
    return np.array(binary_mask)

def create_wordcloud(text, mask_array, output_path, colormap="viridis"):
    """
    Generates and saves the word cloud image.
    """
    wc = WordCloud(
        background_color="white",
        mask=mask_array,
        contour_width=1,
        contour_color="black",
        colormap=colormap
    ).generate(text)

    wc.to_file(output_path)
    print(f"✅ Word cloud saved to: {output_path}")

    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Generate a word cloud in the shape of any image!

        Example usage:
            python wordcloud_cli.py --text "AI ML Python" --image heart.png --output heartcloud.png

        Arguments:
            --text     Use raw text (or specify --text_file instead).
            --text_file Path to a text file containing words.
            --image    Path to the shape image (any format — color or grayscale).
            --output   Output filename for the word cloud image.
            --threshold Threshold (0-255) to extract shape from image (default: 128).
            --invert   Invert image brightness (use if your shape is darker than background).
            --colormap Matplotlib colormap for the word cloud (default: viridis).
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--text", type=str, help="Raw text string for the word cloud.")
    parser.add_argument("--text_file", type=str, help="Path to a .txt file with content.")
    parser.add_argument("--image", type=str, required=True, help="Path to the shape image.")
    parser.add_argument("--output", type=str, default="wordcloud_output.png", help="Output image path.")
    parser.add_argument("--threshold", type=int, default=128, help="Threshold for shape extraction.")
    parser.add_argument("--invert", action="store_true", help="Invert image brightness before processing.")
    parser.add_argument("--colormap", type=str, default="viridis", help="Matplotlib colormap (e.g., plasma, cool, inferno).")

    return parser.parse_args()

def main():
    args = parse_args()

    # Get text input
    if args.text_file:
        if not os.path.exists(args.text_file):
            raise FileNotFoundError(f"Text file not found: {args.text_file}")
        with open(args.text_file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        raise ValueError("You must provide either --text or --text_file.")

    # Check image
    if not os.path.exists(args.image):
        raise FileNotFoundError(f"Image not found: {args.image}")

    # Process mask
    mask_array = preprocess_image(args.image, threshold=args.threshold, invert=args.invert)

    # Create word cloud
    create_wordcloud(text, mask_array, args.output, colormap=args.colormap)

if __name__ == "__main__":
    main()
