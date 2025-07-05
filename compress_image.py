import os
from PIL import Image
import io
import argparse

def compress_image(input_path, output_path, target_size_kb, max_iterations=20, quality=85, tolerance=5):
    """
    Compress an image to approximately match the target file size (in KB).
    
    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the compressed image.
        target_size_kb (float): Desired file size in kilobytes.
        max_iterations (int): Maximum number of compression attempts.
        quality (int): Initial JPEG quality (1-100).
        tolerance (float): Acceptable percentage difference from target size.
    
    Returns:
        tuple: (success: bool, actual_size_kb: float, iterations: int)
    """
    # Convert target size to bytes
    target_size_bytes = target_size_kb * 1024
    
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if image is in RGBA or other modes
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Initialize variables for binary search
            low = 1
            high = 95
            best_quality = quality
            best_size = float('inf')
            iterations = 0
            
            for _ in range(max_iterations):
                iterations += 1
                
                # Save image to memory buffer to check size
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=quality, optimize=True)
                current_size = buffer.tell()
                
                # Check if we're within tolerance
                size_diff = abs(current_size - target_size_bytes)
                size_diff_percent = (size_diff / target_size_bytes) * 100
                
                if size_diff_percent <= tolerance:
                    # Found acceptable quality - save to file
                    with open(output_path, 'wb') as f:
                        f.write(buffer.getvalue())
                    return True, current_size / 1024, iterations
                
                # Update best quality if this is closer to target
                if abs(current_size - target_size_bytes) < abs(best_size - target_size_bytes):
                    best_quality = quality
                    best_size = current_size
                
                # Adjust quality using binary search
                if current_size > target_size_bytes:
                    high = quality - 1
                else:
                    low = quality + 1
                
                # Check if search range is exhausted
                if low > high:
                    break
                
                quality = (low + high) // 2
            
            # If we didn't find within tolerance, use the best we found
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=best_quality, optimize=True)
            with open(output_path, 'wb') as f:
                f.write(buffer.getvalue())
            
            return False, best_size / 1024, iterations
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return False, 0, 0

def main():
    parser = argparse.ArgumentParser(description='Image compression tool')
    parser.add_argument('input', help='Input image file path')
    parser.add_argument('output', help='Output image file path')
    parser.add_argument('size', type=float, help='Target file size in KB')
    parser.add_argument('--quality', type=int, default=85, help='Initial JPEG quality (1-100)')
    parser.add_argument('--tolerance', type=float, default=5, 
                       help='Acceptable percentage difference from target size (default: 5%%)')
    parser.add_argument('--max-iter', type=int, default=20, 
                       help='Maximum compression iterations (default: 20)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        return
    
    print(f"Compressing '{args.input}' to approximately {args.size} KB...")
    
    success, actual_size, iterations = compress_image(
        args.input,
        args.output,
        args.size,
        max_iterations=args.max_iter,
        quality=args.quality,
        tolerance=args.tolerance
    )
    
    if success:
        print(f"Success! Compressed to {actual_size:.2f} KB in {iterations} iterations.")
    else:
        print(f"Best effort: Compressed to {actual_size:.2f} KB in {iterations} iterations (target: {args.size} KB).")
    
    print(f"Output saved to '{args.output}'")

if __name__ == '__main__':
    main()