import customtkinter as ctk
from tkinter import messagebox
import requests

# API URL for similarity endpoint
API_URL = "http://127.0.0.1:8001/similarity"

# Create a requests session and disable environment proxy usage
session = requests.Session()
session.trust_env = False

# Set appearance and theme for CustomTkinter
ctk.set_appearance_mode("dark")          # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")      # Options: "green", "dark-blue"

# Create main window
box = ctk.CTk()
box.title("Sentence Similarity App")

box_width = 600
box_height = 500

screen_width = box.winfo_screenwidth()
screen_height = box.winfo_screenheight()
x = (screen_width // 2) - (box_width // 2)+100
y = (screen_height // 2) - (box_height // 2)

box.geometry(f"{box_width}x{box_height}+{x}+{y}")


# Label and entry for the source sentence
ctk.CTkLabel(box, text="Source Sentence", font=("Arial", 14)).pack(pady=10)
source_entry = ctk.CTkEntry(box, width=500)
source_entry.pack(pady=5)

# Label and textbox for other sentences (comma-separated)
ctk.CTkLabel(box, text="Other Sentences (comma separated)", font=("Arial", 14)).pack(pady=10)
other_text = ctk.CTkTextbox(box, width=500, height=200)
other_text.pack(pady=5)

# Function to call API and compute similarity
def check_similarity():
    # Get input values
    source = source_entry.get().strip()
    others = other_text.get("1.0", "end").strip().split(",")
    others = [s.strip() for s in others if s.strip()]  # Clean empty strings

    # Validate input
    if not source:
        messagebox.showerror("Error", "Source sentence is required!")
        return

    if not others:
        messagebox.showerror("Error", "Enter at least one other sentence!")
        return

    try:
        # Prepare payload for API
        payload = {
            "source_sentence": source,
            "other_sentences": others
        }

        # Call the API
        response = session.post(API_URL, json=payload, timeout=20)
        response.raise_for_status()  # Raise error if HTTP status >=400

        data = response.json()

        # Handle API error
        if "error" in data:
            messagebox.showerror("API Error", data["error"])
            return

        # Format results
        result_text = ""
        for item in data["result"]:
            result_text += f"{item['sentence']} → {item['similarity']:.3f}\n"

        # Show results
        messagebox.showinfo("Similarity Results", result_text)

    except Exception as e:
        # Handle connection or unexpected errors
        messagebox.showerror("Connection Error", f"Cannot connect to API:\n{e}")

# Button to trigger similarity check
ctk.CTkButton(box, text="Check Similarity", command=check_similarity,hover_color="green").pack(pady=20)

# Start the GUI loop
box.mainloop()
