from pathlib import Path
import base64
import filetype


CHARACTER_FILES = [
    Path("characters/monika.chr"),
    Path("characters/natsuki.chr"),
    Path("characters/sayori.chr"),
    Path("characters/yuri.chr"),
]

STAGED_DIR = Path("staged")


def read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def is_valid_base64(data: bytes) -> bool:
    try:
        base64.b64decode(data, validate=True)
        return True
    except (ValueError, base64.binascii.Error):
        return False


def detect_file_type(path: Path):
    kind = filetype.guess(path)
    if not kind:
        return None
    return kind.extension, kind.mime


def save_bytes(data: bytes, directory: Path, filename: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    output_path = directory / filename
    output_path.write_bytes(data)
    print(f"Saved: {output_path}")


def process_character_file(path: Path) -> None:
    print(f"\nAnalyzing: {path}")

    data = read_bytes(path)
    character = path.stem
    staged_character_dir = STAGED_DIR / character

    print(f"First 32 bytes: {data[:32]}")

    file_info = detect_file_type(path)

    if file_info:
        ext, mime = file_info
        print(f"Detected type: {ext} ({mime})")
        save_bytes(data, staged_character_dir, f"0_{character}.{ext}")
        return

    if is_valid_base64(data):
        decoded = base64.b64decode(data)
        save_bytes(decoded, staged_character_dir, "result.txt")
        print(f"\nExtracted valid Base64 data to staged/{character}/result.txt")
        return

    print("Unknown file format and invalid Base64")


def main() -> None:
    for path in CHARACTER_FILES:
        if path.exists():
            process_character_file(path)
        else:
            print(f"Missing file: {path}")


if __name__ == "__main__":
    main()
