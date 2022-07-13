from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from VoightKampffTestBackend import response_generator

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
    questions = {1: "Every country is an animal. What animal is your country?",
                 2: "If you could have the answer to one question, what would it be?",
                 3: "The Supreme Court has overturned roe vs Wade. How do you feel?",
                 4: "What improved your quality of life so much, you wish you did it sooner?",
                 5: "What's a weird thing you think only you do?",
                 6: "What's the worst alcoholic beverage?",
                 7: "Without saying the name, what's your favourite video game?",
                 8: "You can get the attention of the whole planet, but only for ten seconds. What do you say?",
                 9: "You wake up tomorrow with Jeff Bezo's current net worth ($209 Billion USD). What do you do?"}

    return {"question": questions.get(random_int)}

@app.get("/response")
def response(question):
    sess = response_generator.Response().get_model()
    answer = response_generator.Response().get_response(sess=sess, prompt=question)
    return {"response": answer.rpartition('?')[2]}
