import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import nltk
nltk.download('punkt_tab')
from nltk.corpus import stopwords
import re
import tkinter as tk
from tkinter import messagebox

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Common scam keywords
SCAM_KEYWORDS = [
    "quick money", "work from home", "no experience needed",
    "pay upfront", "immediate start", "urgent hire", "click here",
    "bank details", "personal information"
]

# Function to clean and tokenize text
def clean_text(text):
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize and remove stopwords
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word not in stop_words]

# Function to check for scam keywords
def contains_scam_keywords(text):
    tokens = clean_text(text)
    for keyword in SCAM_KEYWORDS:
        if keyword in ' '.join(tokens):
            return True
    return False

# Function to verify the domain
def verify_domain(url):
    try:
        # Extract the domain
        domain = urlparse(url).netloc
        # Perform a simple check on the domain
        # In a real scenario, use an API to validate the domain
        if domain.endswith('.com') or domain.endswith('.org'):
            return True
        else:
            return False
    except Exception as e:
        return False

# Function to analyze the job listing
def analyze_job_listing():
    url = url_entry.get()
    try:
        # Fetch the page content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the job description text
        job_description = soup.get_text()
        
        # Track analysis results
        scam_keyword_found = contains_scam_keywords(job_description)
        domain_verified = verify_domain(url)

        # Determine overall safety
        if scam_keyword_found or not domain_verified:
            result_message = "Warning: This job application is unsafe."
        else:
            result_message = "This job application appears to be safe."
        
        # Display the result in a message box
        messagebox.showinfo("Job Application Analysis", result_message + "\nTip: Do not provide personal information or payment details during the initial job application process.")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error analyzing job listing: {e}")

# Create the GUI application
root = tk.Tk()
root.title("Job Security Scanner")
root.geometry("500x400")

# URL entry field
url_label = tk.Label(root, text="Enter Job Listing URL:")
url_label.pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Analyze button
analyze_button = tk.Button(root, text="Analyze", command=analyze_job_listing)
analyze_button.pack(pady=20)

# Run the GUI application
root.mainloop()


