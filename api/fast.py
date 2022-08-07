from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
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

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>Voight-Kampff Test Response</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        answer = response(data)["response"]
        await websocket.send_text(f"{answer}")

@app.get("/role")
def role():
    random_int = np.random.randint(1,100)
    if random_int % 2 == 0:
        role = True
    else:
        role = False

    return {'role': role}

@app.get("/question")
def question():
    random_int = np.random.randint(1, 6)
    questions = {1: "What improved your quality of life so much, you wish you did it sooner?",
                 2: "What's a weird thing you think only you do?",
                 3: "What's the worst alcoholic beverage?",
                 4: "Without saying the name, what's your favourite video game?",
                 5: "You wake up tomorrow with Jeff Bezo's current net worth ($209 Billion USD). What do you do?"}

    return {"question": questions.get(random_int)}

@app.get("/response")

def response(question):
    sess = response_generator.Response().get_model(run_name='run3')
    top_k = np.random.randint(4000, 6000)
    temperature = np.random.uniform(0.6, 0.9)

    answer = response_generator.Response().get_response(sess=sess, prompt=question, length=200, top_k=top_k, temperature=temperature, run_name='run3')
    return {"response": answer}

if __name__ == "__main__":
    question = question()["question"]
    response = response(question)["response"]
    print(question)
    print(response)
