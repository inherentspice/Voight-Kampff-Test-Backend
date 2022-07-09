from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"greeting": "Welcome to the Voight-Kampff Test API"}

@app.get("/question")
def question():
    random_int = np.random.randint(1, 9)
    questions = {1: "How do you know if you’re in love?",
                 2: "Which came first, the chicken or the egg?",
                 3: "You’re stuck for 24 hours in the last video game you played. What will you be doing during this time?",
                 4: "If you had a gun pointed at your head, what would be your last words?",
                 5: "Why are you here and not somewhere else?",
                 6: "Your objective is to go back into time in the 1700s and blow the minds of everyone there. What do you bring and why?",
                 7: "What’s something most people love, but you hate?",
                 8: "You get teleported to the day you were born with all the memories from your past life, but you’re now an infant. What do you do?}"}

    return {"question": questions.get(random_int)}
