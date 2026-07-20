"""
gui.py
Desktop GUI for the weather tool, built with tkinter (built into Python).
Reuses weather.py exactly as the CLI does — the logic layer doesn't
know or care whether it's being called from a terminal or a window.
"""

import tkinter as tk
from tkinter import ttk
from weather import lookup


class WeatherApp:
    def __init__(self, root):
        self.root = root
        root.title("Weather Lookup")
        root.geometry("320x220")
        root.resizable(False, False)

        # --- Input row ---
        input_frame = ttk.Frame(root, padding=12)
        input_frame.pack(fill="x")

        self.city_entry = ttk.Entry(input_frame)
        self.city_entry.pack(side="left", fill="x", expand=True)
        self.city_entry.bind("<Return>", lambda event: self.search())  # Enter key triggers search

        search_btn = ttk.Button(input_frame, text="Search", command=self.search)
        search_btn.pack(side="left", padx=(8, 0))

        # --- Result area ---
        self.result_label = ttk.Label(
            root, text="Enter a city and press Search",
            padding=12, justify="left", wraplength=280
        )
        self.result_label.pack(fill="both", expand=True)

    def search(self):
        city = self.city_entry.get().strip()
        if not city:
            self.result_label.config(text="Please enter a city name.")
            return

        self.result_label.config(text="Loading...")
        self.root.update_idletasks()  # force the "Loading..." text to render before the network call blocks

        try:
            report = lookup(city)
        except ValueError as e:
            self.result_label.config(text=str(e))
            return
        except Exception:
            self.result_label.config(text="Something went wrong reaching the weather service.")
            return

        self.result_label.config(text=(
            f"{report['name']}\n\n"
            f"Condition:  {report['condition']}\n"
            f"Temp:       {report['temperature_c']}°C\n"
            f"Wind:       {report['windspeed_kmh']} km/h"
        ))


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()