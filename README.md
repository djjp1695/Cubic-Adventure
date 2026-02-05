# Cubic Adventure

**Cubic Adventure** est un petit jeu de plateforme conçu en **Python**, utilisant **PyGame** pour le gameplay et **PyGame-Menu** pour les menus.

---
## Source des sons
Toute la musique et les sons proviennent de https://pixabay.com/sound-effects/

## Prérequis

- Python 3.8 ou supérieur (Python 3.13 max, car Pygame ne supporte pas 3.14 à ce moment)
- PyGame
- PyGame-Menu

> Il est recommandé d’utiliser un environnement virtuel pour gérer les dépendances.

---
## Vidéo du jeu
- Disponible sur Youtube
  - https://www.youtube.com/watch?v=R3Ij1cELoLQ

## Installation

1. **Créer un environnement virtuel :**

```bash
python -m venv venv
```

2. **Activer l’environnement virtuel :**
    - **Windows :** 
    ```bash 
    .\venv\Scripts\activate.bat 
    ```
   - **Linux :**
   ```bash
   source venv/bin/activate
    ```
   - **Mac :**
   ```bash
   source venv/bin/activate
   ```
3. **Installer les dépendance:**
    ```bash
    pip install -r requirements.txt
   ```
4. **Compilation du jeu:**
    ```bash
   python compile.py
   ```
5. **Éxécution du jeu:**
   - Le jeu va être dans le dossier du projet, dans le sous-dossier dist
   - L'éxécutable s'appelle **main.exe**
