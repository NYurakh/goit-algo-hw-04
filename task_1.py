import argparse
import shutil
from pathlib import Path


def copy_files(source: Path, destination: Path) -> None:
    try:
        items = list(source.iterdir())
    except OSError as e:
        print(f"Cannot read directory {source}: {e}.")
        return

    for item in items:
        try:
            if item.is_symlink():
                continue  # * symlinks are skipped to avoid loops

            if item.is_dir():
                copy_files(item, destination)
            elif item.is_file():
                extension = item.suffix.lower().lstrip(".") or "no_extension"
                target_dir = destination / extension
                target_dir.mkdir(parents=True, exist_ok=True)

                target_file = target_dir / item.name
                counter = 1
                while target_file.exists():
                    target_file = target_dir / f"{item.stem}_{counter}{item.suffix}"
                    counter += 1

                shutil.copy2(item, target_file)
                print(f"Copied: {item} -> {target_file}")
        except PermissionError as e:
            print(f"Permission denied: {item}: {e}.")  # ! one bad file must not stop the rest
        except OSError as e:
            print(f"File system error: {item}: {e}.")

def main():
    parser = argparse.ArgumentParser(
        description="Recursively copy and sort files by extension."
    )
    parser.add_argument("source", type=Path, help="Source directory")
    parser.add_argument(
        "destination",
        nargs="?",
        type=Path,
        default=Path("dist"),
        help="Destination directory (default: 'dist')",
    )

    args = parser.parse_args()

    source = args.source.resolve()
    destination = args.destination.resolve()

    if not source.is_dir():
        parser.error("Source directory does not exist.")

    if destination == source or destination.is_relative_to(source):
        parser.error("Destination must be outside the source directory.")

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        parser.error(f"Cannot create destination: {error}")

    copy_files(source, destination)
    print("Copying completed.")


if __name__ == "__main__":
    main()
