import customtkinter as ctk  # Using customtkinter for a modern UI
import subprocess  # To run separate server and UI scripts
import sys  # To get the Python executable path
import time  # For timing or delays (currently unused)
import requests  # To check if servers are running
from tkinter import messagebox  # For showing error messages

# Set appearance and color theme
ctk.set_appearance_mode("light")  # Other appearance modes: "light", "system" 
ctk.set_default_color_theme("blue")  #Other color themes: "green", "dark-blue"

# Create the main application window
app = ctk.CTk()
app.title("AI Tools Menu")

app_width = 600
app_height = 300

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width // 2) - (app_width // 2)+100
y = (screen_height // 2) - (app_height // 2)

app.geometry(f"{app_width}x{app_height}+{x}+{y}")


# Start the backend servers for similarity and sentiment analysis
similarity_server = subprocess.Popen([sys.executable, "similarityServer.py"])
sentiment_server = subprocess.Popen([sys.executable, "sentimentServer.py"])

# Function to run the Sentence Similarity UI
def run_similarity():
    try:
        # Check if the similarity server is running
        requests.get("http://127.0.0.1:8001", timeout=2)
        # If server is running, open the similarity UI
        subprocess.Popen([sys.executable, "similarityUi.py"])
    except:
        # Show an error message if the server is not available
        messagebox.showerror("Server Error", "Similarity Server not running!")

# Function to run the Sentiment Analysis UI
def run_sentiment():
    try:
        # Check if the sentiment server is running
        requests.get("http://127.0.0.1:8000", timeout=2)
        # If server is running, open the sentiment UI
        subprocess.Popen([sys.executable, "sentimentUi.py"])
    except:
        # Show an error message if the server is not available
        messagebox.showerror("Server Error", "Sentiment Server not running!")

# Add label and buttons to the main window
ctk.CTkLabel(app, text="Choose a tool", font=("Arial", 18)).pack(pady=20)
ctk.CTkButton(app, text="Sentence Similarity", command=run_similarity, width=200, height=50,hover_color="green").pack(pady=20)
ctk.CTkButton(app, text="Sentiment Analysis", command=run_sentiment, width=200, height=50,hover_color="green").pack(pady=20)

# Start the main event loop
app.mainloop()
