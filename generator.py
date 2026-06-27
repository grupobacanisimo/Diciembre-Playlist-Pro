import os
import random
from pathlib import Path

AUDIO_EXTENSIONS = (".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a")


class PlaylistGenerator:
    def __init__(self, config):
        self.config = config
        self.cycle_cache = {}
        self.used_files = set()

    def scan_folder(self, folder_path):
        """Escanea carpeta y subcarpetas"""
        files = []
        for root, _, filenames in os.walk(folder_path):
            for f in filenames:
                if f.lower().endswith(AUDIO_EXTENSIONS):
                    files.append(os.path.join(root, f))
        return files

    def get_next_song(self, category, folder_path):
        """
        Devuelve canción sin repetir hasta agotar carpeta
        """
        if category not in self.cycle_cache or len(self.cycle_cache[category]) == 0:
            all_files = self.scan_folder(folder_path)

            # eliminar usados en este ciclo si aún hay disponibles
            available = [f for f in all_files if f not in self.used_files]

            if not available:
                # reiniciar ciclo
                self.used_files = set()
                available = all_files

            random.shuffle(available)
            self.cycle_cache[category] = available

        song = self.cycle_cache[category].pop()
        self.used_files.add(song)
        return song

    def get_random_simple(self, folder_path):
        """IDs, promos y comerciales (pueden repetirse)"""
        files = self.scan_folder(folder_path)
        if not files:
            return None
        return random.choice(files)

    def generate(self, sequence, folders, output_path, total_items=100):
        """
        Genera playlist M3U según secuencia
        """
        playlist = []
        index = 0

        for _ in range(total_items):
            step = sequence[index % len(sequence)]
            index += 1

            if step not in folders:
                continue

            folder = folders[step]

            if step.lower() in ["id", "promo", "comercial"]:
                song = self.get_random_simple(folder)
            else:
                song = self.get_next_song(step, folder)

            if song:
                playlist.append(song)

        # guardar M3U
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for item in playlist:
                f.write(item + "\n")

        return playlist
