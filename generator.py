import os
import random
import unicodedata

AUDIO_EXTENSIONS = (".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a")


class PlaylistGenerator:
    def __init__(self):
        self.cycle_cache = {}
        self.used_files = set()

    def clean_name(self, name):
        """Quita caracteres raros para M3U"""
        nfkd = unicodedata.normalize('NFKD', name)
        return "".join([c for c in nfkd if not unicodedata.combining(c)])

    def scan_folder(self, folder_path):
        files = []

        if not folder_path or not os.path.exists(folder_path):
            return files

        for root, _, filenames in os.walk(folder_path):
            for f in filenames:
                if f.lower().endswith(AUDIO_EXTENSIONS):
                    files.append(os.path.join(root, f))

        return files

    def get_next_song(self, category, folder_path):
        if category not in self.cycle_cache or len(self.cycle_cache[category]) == 0:
            all_files = self.scan_folder(folder_path)

            if not all_files:
                return None

            available = [f for f in all_files if f not in self.used_files]

            if not available:
                self.used_files.clear()
                available = all_files

            random.shuffle(available)
            self.cycle_cache[category] = available

        song = self.cycle_cache[category].pop()
        self.used_files.add(song)
        return song

    def get_random_simple(self, folder_path):
        files = self.scan_folder(folder_path)
        if not files:
            return None
        return random.choice(files)

    def generate(self, sequence, folders, output_path, total_items=100):
        playlist = []

        if not folders:
            return []

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

        # guardar M3U limpio
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")

                for item in playlist:
                    name = self.clean_name(os.path.basename(item))
                    f.write(f"#EXTINF:-1,{name}\n")
                    f.write(f"{item}\n")

        except Exception as e:
            print("Error M3U:", e)

        return playlist
