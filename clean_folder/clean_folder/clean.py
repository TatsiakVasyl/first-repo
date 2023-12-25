import sys
from pathlib import Path
import shutil
import re

def normalize(name: str) -> str:
    uk_symbols = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
    translation = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

    trans = {}
    for key, value in zip(uk_symbols, translation):
        trans[ord(key)] = value
        trans[ord(key.upper())] = value.upper()

    name, *extension = name.split('.')
    new_name = name.translate(trans)
    new_name = re.sub(r'\W', '_', new_name)
    return f"{new_name}.{'.'.join(extension)}"

def handle_file(file_path, root_folder, category, known_extensions, unknown_extensions):
    target_folder = root_folder / category
    target_folder.mkdir(exist_ok=True)
    new_name = normalize(file_path.name)
    file_path.replace(target_folder / new_name)

    extension = file_path.suffix[1:].upper()
    if extension:
        known_extensions.add(extension)
    else:
        unknown_extensions.add('')

def handle_archive(archive_path, root_folder, category, known_extensions, unknown_extensions):
    target_folder = root_folder / category
    target_folder.mkdir(exist_ok=True)
    
    new_name = normalize(archive_path.stem)
    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(archive_path.resolve()), str(archive_folder.resolve()))
        known_extensions.add(archive_folder.suffix[1:].upper())
    except shutil.ReadError:
        archive_folder.rmdir()
        unknown_extensions.add('')

def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def process_folder(folder, known_extensions, unknown_extensions):
    for item in folder.iterdir():
        if item.is_dir():
            process_folder(item, known_extensions, unknown_extensions)
        else:
            handle_file_or_archive(item, folder, known_extensions, unknown_extensions)

def handle_file_or_archive(item, folder, known_extensions, unknown_extensions):
    extension = item.suffix[1:].upper()
    if extension in ('JPEG', 'PNG', 'JPG', 'SVG'):
        handle_file(item, folder, 'images', known_extensions, unknown_extensions)
    elif extension in ('AVI', 'MP4', 'MOV', 'MKV'):
        handle_file(item, folder, 'video', known_extensions, unknown_extensions)
    elif extension in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
        handle_file(item, folder, 'documents', known_extensions, unknown_extensions)
    elif extension in ('MP3', 'OGG', 'WAV', 'AMR'):
        handle_file(item, folder, 'audio', known_extensions, unknown_extensions)
    elif extension in ('ZIP', 'GZ', 'TAR'):
        handle_archive(item, folder, 'archives', known_extensions, unknown_extensions)
    else:
        handle_file(item, folder, 'other', known_extensions, unknown_extensions)

def print_results(known_extensions, unknown_extensions, categories):
    print("Known Extensions:", known_extensions)
    print("Unknown Extensions:", unknown_extensions)

    for category in categories:
        print(f"\n{category.capitalize()} Files:")
        files = list(Path(category).rglob("*"))
        if files:
            for file in files:
                print(file)
        else:
            print("No files in this category.")

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    print(f'Starting in {path}')

    target_folder = Path(path)
    target_folder.mkdir(exist_ok=True)

    known_extensions = set()
    unknown_extensions = set()

    categories = ['images', 'video', 'documents', 'audio', 'archives', 'other']

    for category in categories:
        category_folder = target_folder / category
        category_folder.mkdir(exist_ok=True)

    process_folder(target_folder, known_extensions, unknown_extensions)
    remove_empty_folders(target_folder)

    print_results(known_extensions, unknown_extensions, categories)

if __name__ == '__main__':
    main()