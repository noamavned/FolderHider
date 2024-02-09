import time
import os
from tkinter import filedialog


def ClearScreen() -> None:
    """Clear the terminal for better user experience
    """
    os.system("cls || clear")


def ShowLogo() -> None:
    """Print logo of project and name of creator (Noam Abend -> CHEF)
    """
    ClearScreen()
    print(f"┌──────────────────────────────────────────────────────────────┐")
    print(f"│  ────  ────  ────  ────  ────  ────  ────  ────  ────  ────  │")
    print(f"│                                                              │")
    print(f"│  ╔═════   ╔══════╗   ║          ╔════╗     ╔═════   ╔════╗   │")
    print(f"│  ║        ║      ║   ║          ║     ╚╗   ║        ║    ║   │")
    print(f"│  ╠═════   ║      ║   ║          ║     ╔╝   ╠═════   ╠═══╦╝   │")
    print(f"│  ║        ║      ║   ║          ║    ╔╝    ║        ║   ╚╗   │")
    print(f"│  ║        ╚══════╝   ╚═══════   ╚═══╝      ╚═════   ║    ║   │")
    print(f"│                                                              │")
    print(f"│  ║     ║   ═╦═   ╔════╗     ╔═════   ╔════╗                  │")
    print(f"│  ║     ║    ║    ║     ╚╗   ║        ║    ║                  │")
    print(f"│  ╠═════╣    ║    ║     ╔╝   ╠═════   ╠═══╦╝                  │")
    print(f"│  ║     ║    ║    ║    ╔╝    ║        ║   ╚╗                  │")
    print(f"│  ║     ║   ═╩═   ╚═══╝      ╚═════   ║    ║                  │")
    print(f"│                                                              │")
    print(f"│  ────  ────  ────  ────  ────  ────  ────  ────  ────  ────  │")
    print(f"│                                                              │")
    print(f"│  ╔═════   ║     ║   ╔═════   ╔═════                          │")
    print(f"│  ║        ║     ║   ║        ║                               │")
    print(f"│  ║        ╠═════╣   ╠═════   ╠═════                          │")
    print(f"│  ║        ║     ║   ║        ║                               │")
    print(f"│  ╚═════   ║     ║   ╚═════   ║                               │")
    print(f"│                                                       <···>  │")
    print(f"│  ────  ────  ────  ────  ────  ────  ────  ────  ────  ────  │")
    print(f"└──────────────────────────────────────────────────────────────┘")


def confirm(s: str) -> bool:
    """Confirm user input

    Args:
        s (str): user input

    Returns:
        bool: whether user confirmed or not
    """
    r = True
    while r:
        ans = input(f"{s}\nConfirm? (Y/N): ").lower()
        if ans not in ["y", "n", ""]:
            ClearScreen()
            print("Not a legitimate answer.")
            time.sleep(1)
            ClearScreen()
        else:
            r = False
    return ans == "y" or ans == ""


def pathExists(path: str) -> bool:
    """Check if path exists

    Args:
        path (str): Path to check

    Returns:
        bool: Does path exist
    """
    return os.path.exists(path)


def createBatch(password: str, folderName: str) -> str:
    """Create batch file's content

    Args:
        password (str): password
        folderName (str): folder name

    Returns:
        str: batch file's content
    """
    return f"""@echo off
setlocal enabledelayedexpansion

set "password={password}"
set "folderName={folderName}"

set /p "enteredPassword=Enter the password: "

if !enteredPassword! equ !password! (
    if exist "%folderName%" (
        echo Folder found. Creating and hiding zip...
        7z a -tzip -p"%password%" "%folderName%.zip" "%folderName%" > nul
        attrib +h "%folderName%.zip"
        rd /s /q "%folderName%"
        echo Folder is now hidden.
    ) else (
        echo Folder not found. Reverting zip...
        7z x -tzip -p"%password%" "%folderName%.zip" > nul
        attrib -h "%folderName%.zip"
        del /q "%folderName%.zip"
        echo Folder is now visible.
    )
) else (
    echo Incorrect password. Exiting program...
)

endlocal"""


def main() -> None:
    """Main function of program
    """
    # show logo #
    ShowLogo()
    time.sleep(1.25)

    # ask for parent path #
    selected = False
    parent_path = ""
    while not selected:
        ClearScreen()
        parent_path = filedialog.askdirectory()
        ClearScreen()
        if (parent_path == ""):
            print("No path selected.")
            time.sleep(2)
        else:
            selected = confirm(parent_path)

    # ask for new path's name #
    path_name = ""
    selected = False
    while not selected:
        ClearScreen()
        path_name = input("Enter name of new folder: ")
        ClearScreen()
        if (path_name == ""):
            print("No path name selected.")
            time.sleep(2)
        else:
            selected = confirm(path_name)

    # check full path and add _int to not write over existing folder #
    full_path = os.path.join(parent_path, path_name)
    if (path_name != ""):
        TEMP = full_path
        i = 0
        while (pathExists(TEMP)):
            i += 1
            TEMP = os.path.join(parent_path, path_name + "_" + str(i))
        full_path = TEMP

    # ask for password #
    password = ""
    selected = False
    while not selected:
        ClearScreen()
        password = input("Enter password: ")
        ClearScreen()
        selected = confirm(password)

    # create path #
    os.mkdir(full_path)

    # creating batch file and printing message #
    with open(os.path.join(parent_path, f"FolderSetup{time.strftime('-%Y-%m-%d')}.bat"), "w") as f:
        f.write(createBatch(password, path_name))

    ClearScreen()
    print("Generated folder with batch file.\nNotice that the folder is not hidden when setting up.\nThe batch file has to be in the same folder as the folder you want to hide/show.")


if __name__ == "__main__":
    main()
