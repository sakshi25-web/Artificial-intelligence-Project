import pandas as pd
import nltk
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "faq.csv")

data = pd.read_csv(csv_path)

# Load FAQ dataset
# data = pd.read_csv("faq.csv")

questions = data["Question"].tolist()
answers = data["Answer"].tolist()

lemmatizer = WordNetLemmatizer()

# Text preprocessing
def preprocess(text):
    text = text.lower()

    tokens = text.split()

    tokens = [
        word for word in tokens
        if word not in string.punctuation
    ]

    tokens = [
        word for word in tokens
        if word not in stopwords.words("english")
    ]

    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]

    return " ".join(tokens)

processed_questions = [preprocess(q) for q in questions]

vectorizer = TfidfVectorizer()

faq_vectors = vectorizer.fit_transform(processed_questions)


# GUI for the chatbot
import customtkinter as ctk
from datetime import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("AI FAQ Chatbot")
root.geometry("850x650")

title = ctk.CTkLabel(
    root,
    text="🤖 AI FAQ Chatbot",
    font=("Arial",24,"bold")
)
title.pack(pady=15)

chat_box = ctk.CTkTextbox(root,width=780,height=420,font=("Arial",14))
chat_box.pack(pady=10)
chat_box.configure(state="disabled")

entry = ctk.CTkEntry(
    root,
    width=600,
    placeholder_text="Ask your question..."
)
entry.pack(side="left",padx=20,pady=20)

def send():

    question = entry.get().strip()

    if question=="":
        return

    processed = preprocess(question)

    user_vector = vectorizer.transform([processed])

    similarity = cosine_similarity(user_vector,faq_vectors)

    best = similarity.argmax()

    score = similarity[0][best]

    time = datetime.now().strftime("%H:%M:%S")

    chat_box.configure(state="normal")

    chat_box.insert("end",f"\n🧑 [{time}] You : {question}\n")

    if score>0.30:

        confidence=round(score*100,2)

        chat_box.insert(
            "end",
            f"🤖 Bot : {answers[best]}\n"
        )

        chat_box.insert(
            "end",
            f"Confidence : {confidence}%\n\n"
        )

    else:

        chat_box.insert(
            "end",
            "🤖 Bot : Sorry, I couldn't understand your question.\n\n"
        )

    chat_box.configure(state="disabled")

    entry.delete(0,"end")

send_button=ctk.CTkButton(
    root,
    text="Send",
    command=send
)

send_button.pack(side="left",padx=10)

def clear_chat():
    chat_box.configure(state="normal")
    chat_box.delete("1.0","end")
    chat_box.configure(state="disabled")

clear_button=ctk.CTkButton(
    root,
    text="Clear Chat",
    command=clear_chat,
    fg_color="red"
)

clear_button.pack(side="left",padx=10)

entry.bind("<Return>",lambda event:send())

root.mainloop()