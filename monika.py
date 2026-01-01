from pathlib import Path
import base64
from PIL import Image


CROP_SIZE = 141
STAGED_DIR = Path("staged/monika")


def center_crop_box(width: int, height: int, size: int):
    half = size // 2
    cx, cy = width // 2, height // 2
    return (cx - half, cy - half, cx + half, cy + half)


def load_and_crop_image(path: Path, crop_size: int) -> Image.Image | None:
    try:
        with Image.open(path) as img:
            print(f"Format: {img.format}, Size: {img.size}, Mode: {img.mode}")
            return img.crop(center_crop_box(*img.size, crop_size))
    except Exception as e:
        print(f"Image error: {e}")
        return None


def extract_bits_and_bytes(img: Image.Image):
    output = bytearray()
    bits = []

    current_byte = 0
    bit_count = 0

    for pixel in img.getdata():
        r, g, b = pixel[:3]

        if (r, g, b) == (0, 0, 0):
            bit = 0
        elif (r, g, b) == (255, 255, 255):
            bit = 1
        else:
            continue

        bits.append(bit)
        current_byte = (current_byte << 1) | bit
        bit_count += 1

        if bit_count == 8:
            output.append(current_byte)
            current_byte = 0
            bit_count = 0

    return bits, output


def main():
    source_image = Path("characters/monika.chr")
    STAGED_DIR.mkdir(parents=True, exist_ok=True)

    cropped = load_and_crop_image(source_image, CROP_SIZE)
    if not cropped:
        return

    cropped_path = STAGED_DIR / "1_monika_cropped.png"
    cropped.save(cropped_path)
    print(f"Saved cropped image: {cropped_path}")

    bits, byte_data = extract_bits_and_bytes(cropped)

    (STAGED_DIR / "2_monika_bits.txt").write_text("".join(map(str, bits)))
    print("Extracted bits to staged/monika/2_monika_bits.txt")

    (STAGED_DIR / "3_monika_b64.txt").write_bytes(byte_data)
    print("Extracted byte data to staged/monika/3_monika_b64.txt")

    try:
        decoded = base64.b64decode(byte_data)
        (STAGED_DIR / "result.txt").write_bytes(decoded)
        print("Decoded Base64 data to staged/monika/result.txt")
    except Exception as e:
        print(f"Base64 decode failed: {e}")


if __name__ == "__main__":
    main()
