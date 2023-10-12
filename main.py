# main.py

from fastapi import FastAPI, HTTPException, Body
import csv
from typing import List, Optional

app = FastAPI()

# This is our data model, representing the contents of our CSV file.
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


# Route to read all items from the CSV
@app.get("/items/", response_model=List[Item])
def read_items():
    items = []
    with open("data.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            item = Item(id=int(row[0]), name=row[1], description=row[2])
            items.append(item)
    return items


# Route to read a single item from the CSV using its ID
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    with open("data.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if int(row[0]) == item_id:
                return Item(id=int(row[0]), name=row[1], description=row[2])
    raise HTTPException(status_code=404, detail="Item not found")


# Route to add a new item to the CSV
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    with open("data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([item.id, item.name, item.description])
    return item


# Route to update an existing item in the CSV
@app.post("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item = Body(...)):
    items = []
    with open("data.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        items = list(reader)

    found = False
    for index, row in enumerate(items):
        if int(row[0]) == item_id:
            items[index] = [item.id, item.name, item.description]
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="Item not found")

    with open("data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(items)

    return item
