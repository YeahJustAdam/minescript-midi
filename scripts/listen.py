import minescript as ms

def listen_for_minecatrts(x, y, z):
    """ Listen for minecarts passing over the note blocks and play the corresponding notes. """
    iterate = 0
    triggered = set()
    while True:
        carts = ms.get_entities(name="Minecart")
        if carts:
            for cart in carts:
                if cart:
                    mx, my, mz = cart.position
                    mz = int(mz - 0.5)
                    setblock_str = f"setblock {x+26} {y+3} {mz} minecraft:redstone_block"
                    reset_str = f"setblock {x+26} {y+3} {mz} minecraft:air"
                if mx < x+25.5 and mx > x+24.5 and cart.uuid not in triggered:
                    ms.execute(setblock_str)
                    ms.execute(reset_str)
                    triggered.add(cart.uuid)
                if mx > x+35:
                    uuid = cart.uuid
                    ms.execute(f"execute as {uuid} run kill @s")
                    if uuid in triggered:
                        triggered.remove(uuid)

if __name__ == "__main__":
    ms.chat("Starting to listen for minecarts")
    x, y, z = [int(p) for p in ms.player().position]
    x = x + 1
    listen_for_minecatrts(x, y, z)