import mido 
import minescript as ms
import time

carts = ms.get_entities()
entities = ms.entities()
for e in entities:
    strings = f"{e.name}, {e.type}"
    ms.chat(strings)