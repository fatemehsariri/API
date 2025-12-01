import customtkinter as ctk  # Modern Tkinter widgets
from tkinter import messagebox  # For showing message boxes
import requests  # For making HTTP requests to the API

# API endpoint for sentiment analysis
API_URL = "http://127.0.0.1:8000/sentiment"

# Create a session and disable reading proxy settings from environment
session = requests.Session()
session.trust_env = False  # Avoid using Windows proxy settings which may cause errors

# Set the appearance and color theme of the UI
ctk.set_appearance_mode("dark")          # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")      # Options: "green", "dark-blue"

# Create the main application window
app = ctk.CTk()
app.title("Sentiment Analysis App")

app_width = 600
app_height = 400

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width // 2) - (app_width // 2)+100
y = (screen_height // 2) - (app_height // 2)

app.geometry(f"{app_width}x{app_height}+{x}+{y}")



# Label and textbox for user input
ctk.CTkLabel(app, text="Enter English text:", font=("Arial", 14)).pack(pady=10)
text_input = ctk.CTkTextbox(app, width=550, height=150)
text_input.pack(pady=5)

# Function to call the API and display results
def analyze_sentiment():
    text = text_input.get("1.0", "end").strip()  # Get text from textbox
    if not text:
        messagebox.showinfo("Error", "Please enter some text!")  # Alert if empty
        return
    try:
        payload = {"text": text}
        response = session.post(API_URL, json=payload, timeout=30)  # Send request
        response.raise_for_status()  # Raise exception if HTTP error
        data = response.json()

        if "error" in data:  # Check if API returned an error
            messagebox.showerror("API Error", data["error"])
            return

        # Format the result for message box
        result_text = ""
        for item in data["sentiment"]:
            result_text += f"{item['label']} → {item['score']:.3f}\n"

        messagebox.showinfo("Sentiment Result", result_text)

    except Exception as e:
        # Show an error if connection or request fails
        messagebox.showerror("Connection Error", f"Cannot connect to API:\n{e}")

# Button to trigger sentiment analysis
ctk.CTkButton(app, text="Analyze Sentiment", command=analyze_sentiment,hover_color="green").pack(pady=20)

# Run the UI event loop
app.mainloop()
