from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=['ROOT'])
async def root() -> dict:
    return {"Ping": "Pong"}


@app.get('/todo', tags=['todos'])
async def get_todo() -> dict:
    return {"data": todos}


@app.post("/todo", tags=["todos"])
async def add_todo(todo: dict) -> dict:
    todos.append(todo)
    return {
        "data": "A todo has been added successfuly!"
    }


@app.put("/todo/{id}", tags=['todos'])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if int(todo['id']) == id:
            todo['Activity'] = body['Activity']
            return {
                'data': f"Todo with id:{id} has been updated."
            }

    return {
        'data': f"Todo with id:{id} has not been updated."
    }


@app.delete('/todo/{id}', tags=['todos'])
async def delete_todo(id: int) -> dict:
    for todo in todos:
        if int(todo['id']) == id:
            todos.remove(todo)
            return {
                "data": f"id: {id} Todo was removed"
            }
    return {
        "data": f"id: {id} Todo was not removed"
    }


todos = [
    {
        "id": "1",
        "Activity": "Sport at 7pm"
    },
    {
        "id": "2",
        "Activity": "Dinner at 5pm"
    }
]
