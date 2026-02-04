import PyInstaller.__main__
PyInstaller.__main__.run([
    'main.py',              # ton script principal
    '--onefile',            # ou '--onedir' si tu veux un dossier
    '--add-data', 'Assets;Assets',  # <-- inclure le dossier Assets (Windows)
    # '--add-data', 'Assets:Assets',  # <-- si Linux/macOS
])