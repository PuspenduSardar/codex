import argparse
import os
from pdf2image import convert_from_path


def pdf_to_images(input_pdf, output_dir, fmt="png", dpi=200):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Convert PDF pages to images
    images = convert_from_path(input_pdf, dpi=dpi)

    for idx, image in enumerate(images, start=1):
        output_path = os.path.join(output_dir, f"page_{idx}.{fmt}")
        image.save(output_path, fmt.upper())
        print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert PDF to images.")
    parser.add_argument("-i", "--input", required=True, help="Input PDF file path")
    parser.add_argument("-o", "--output", required=True, help="Output directory")
    parser.add_argument("-f", "--format", default="png", choices=["png", "jpeg", "jpg", "tiff", "bmp"],
                        help="Output image format (default: png)")
    parser.add_argument("-d", "--dpi", type=int, default=200, help="Resolution in DPI (default: 200)")

    args = parser.parse_args()

    pdf_to_images(args.input, args.output, fmt=args.format, dpi=args.dpi)


if __name__ == "__main__":
    main()

