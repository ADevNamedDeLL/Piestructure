'''
           _____             _   _                          _ _____       _      _      
     /\   |  __ \           | \ | |                        | |  __ \     | |    | |     
    /  \  | |  | | _____   _|  \| | __ _ _ __ ___   ___  __| | |  | | ___| |    | |     
   / /\ \ | |  | |/ _ \ \ / / . ` |/ _` | '_ ` _ \ / _ \/ _` | |  | |/ _ \ |    | |     
  / ____ \| |__| |  __/\ V /| |\  | (_| | | | | | |  __/ (_| | |__| |  __/ |____| |____ 
 /_/    \_\_____/ \___| \_/ |_| \_|\__,_|_| |_| |_|\___|\__,_|_____/ \___|______|______|   was here . . .
                                                                                        
   
'''
import os
import pathlib
import platform
import time
import re
from colorama import init, Fore

# Initialize colorama for Windows terminal support
init(autoreset=True)

# ANSI color codes for rainbow colors
RAINBOW_COLORS = [
    "\033[31m",  # Red
    "\033[33m",  # Yellow
    "\033[32m",  # Green
    "\033[36m",  # Cyan
    "\033[34m",  # Blue
    "\033[35m",  # Magenta
]

# ASCII Logo
LOGO = r"""
$$$$$$$\  $$\                       $$\                                     $$\                                   
$$  __$$\ \__|                      $$ |                                    $$ |                                  
$$ |  $$ |$$\  $$$$$$\   $$$$$$$\ $$$$$$\    $$$$$$\  $$\   $$\  $$$$$$$\ $$$$$$\   $$\   $$\  $$$$$$\   $$$$$$\  
$$$$$$$  |$$ |$$  __$$\ $$  _____|\_$$  _|  $$  __$$\ $$ |  $$ |$$  _____|\_$$  _|  $$ |  $$ |$$  __$$\ $$  __$$\ 
$$  ____/ $$ |$$$$$$$$ |\$$$$$$\    $$ |    $$ |  \__|$$ |  $$ |$$ /        $$ |    $$ |  $$ |$$ |  \__|$$$$$$$$ |
$$ |      $$ |$$   ____| \____$$\   $$ |$$\ $$ |      $$ |  $$ |$$ |        $$ |$$\ $$ |  $$ |$$ |      $$   ____| 
$$ |      $$ |\$$$$$$$\ $$$$$$$  |  \$$$$  |$$ |      \$$$$$$  |\$$$$$$$\   \$$$$  |\$$$$$$  |$$ |      \$$$$$$$\ 
\__|      \__| \_______|\_______/    \____/ \__|       \______/  \_______|   \____/  \______/ \__|       \_______| 

                                            made by adevnameddell
"""

def rainbow_text(text):
    colored_text = []
    color_count = len(RAINBOW_COLORS)
    color_index = 0
    for char in text:
        if char == "\n":
            colored_text.append(char)
        else:
            colored_text.append(RAINBOW_COLORS[color_index % color_count] + char)
            color_index += 1
    return "".join(colored_text)

def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()

def generate_tree(dir_path, exclude_addresses, prefix=""):
    entries = sorted(os.scandir(dir_path), key=lambda e: (not e.is_dir(), e.name.lower()))
    for index, entry in enumerate(entries):
        # Check if the current entry is in the exclude list
        if entry.path in exclude_addresses:
            continue
        connector = "└── " if index == len(entries) - 1 else "├── "
        yield f"{prefix}{connector}{entry.name}"
        if entry.is_dir(follow_symlinks=False):
            extension = "    " if index == len(entries) - 1 else "│   "
            yield from generate_tree(entry.path, exclude_addresses, prefix + extension)

def make_structure():
    title = input(Fore.WHITE + "Enter title for the output file: ").strip()
    title = sanitize_filename(title)

    if not title:
        print(Fore.RED + "Invalid title. Please enter a valid name.")
        input(Fore.YELLOW + "Press Enter to return to menu...")
        return

    directory = input(Fore.WHITE + "Enter path to the directory (e.g., C:/Users/YourName/Desktop): ").strip()
    directory = os.path.expanduser(directory)

    if not os.path.isdir(directory):
        print(Fore.RED + "Invalid directory path.")
        input(Fore.YELLOW + "Press Enter to return to menu...")
        return

    # Asking for the exclude addresses
    exclude_input = input(Fore.WHITE + "Enter addresses to exclude (comma-separated, leave blank to exclude none): ").strip()
    exclude_addresses = set()

    if exclude_input:
        exclude_addresses = {os.path.expanduser(addr.strip()) for addr in exclude_input.split(",")}
    
    root_name = os.path.basename(os.path.normpath(directory))
    tree_lines = [root_name] + list(generate_tree(directory, exclude_addresses))

    print(Fore.MAGENTA + "\nChoose output option:")
    print(Fore.GREEN + "1. Show only in terminal")
    print(Fore.GREEN + "2. Show and save to file")
    print(Fore.GREEN + "3. Save only (do not show)")

    choice = input("Enter your choice (1-3): ").strip()

    if choice == "1":
        print("\n" + "\n".join(tree_lines))
    elif choice == "2":
        print("\n" + "\n".join(tree_lines))
        save_to_file(title, tree_lines)
    elif choice == "3":
        save_to_file(title, tree_lines)
    else:
        print(Fore.RED + "Invalid choice. Returning to menu.")
        input(Fore.YELLOW + "Press Enter to continue...")
        return

    input(Fore.YELLOW + "\nPress Enter to return to menu...")
    clear_console()

def save_to_file(title, lines):
    script_dir = pathlib.Path(__file__).parent
    exports_dir = script_dir / "exports"
    exports_dir.mkdir(exist_ok=True)
    output_file = exports_dir / f"{title}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nStructure saved to: {output_file}")

def show_about():
    clear_console()
    print(rainbow_text(LOGO))
    print("\n" + "made by adevnameddell using python to keep track of the structure of certain projects".center(100) + "\n")
    input(Fore.YELLOW + "Press Enter to return to menu...")
    clear_console()

def main_menu():
    while True:
        clear_console()
        print(rainbow_text(LOGO))
        print(Fore.MAGENTA + "\nMenu:")
        print("1. Make Structure")
        print("2. About")
        print(Fore.RED + "3. Exit")

        choice = input(Fore.CYAN + "\nEnter your choice (1-3): ").strip()

        if choice == "1":
            clear_console()
            make_structure()
        elif choice == "2":
            show_about()
        elif choice == "3":
            print("Goodbye.")
            time.sleep(1)
            clear_console()
            break
        else:
            print(Fore.RED + "Invalid choice. Try again.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
