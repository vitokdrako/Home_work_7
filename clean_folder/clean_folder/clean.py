import sys
from pathlib import Path
import re
import shutil

TRANSLIT_DICT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh',
    'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
    'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
    'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ю': 'iu', 'я': 'ia'
}


CATEGORIES = {"Audio": [".mp3", ".wav", ".flac", ".wma"],
              "Docs": [".docx", ".txt", ".pdf"],
              "Video": [".mkv", ".flv", ".webm", ".avi", ".wmv", ".mp4"],
              "Picture": [".gif", ".jpg", ".jpeg", ".png"]}

SPECIAL_FOLDERS = ["Audio", "Docs", "Video", "Picture", "Other"]

def normalize(name:str) -> str:
    name = name.lower()
    transliterated = ''.join(TRANSLIT_DICT.get(c, c) for c in name)
    clean_name = re.sub(r'[^a-zA-Z0-9]', '_', transliterated)
    return clean_name

def get_categories(file:Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def move_file(file:Path, category:str, root_dir:Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    
    new_file_name = normalize(file.stem) + file.suffix.lower()
    new_path = target_dir.joinpath(new_file_name)
    
    counter = 1
    while new_path.exists():
        new_file_name = f"{normalize(file.stem)}_{counter}{file.suffix.lower()}"
        new_path = target_dir.joinpath(new_file_name)
        counter += 1
        
    file.replace(new_path)

def sort_folder(path:Path) -> None:
    for element in path.glob("**/*"):
        if element.is_file() and not element.parent.name in SPECIAL_FOLDERS:  
            category = get_categories(element)
            move_file(element, category, path)

    for element in path.glob("**/*"):
        if element.is_dir() and not any(element.iterdir()):
            element.rmdir()

def remove_empty_dirs(path: Path) -> None:
    for element in path.iterdir():
        if element.is_dir():
            remove_empty_dirs(element)
            if not any(element.iterdir()):
                try:
                    element.rmdir()
                except Exception as e:
                    print(f"Error removing directory {element}: {e}")


def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return "Folder dos not exists"
    
    sort_folder(path)
    
    return "All Ok"

if __name__ == '__main__':
    main() 