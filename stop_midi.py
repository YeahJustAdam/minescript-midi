import minescript as ms

ms.execute("\killjob 1")
ms.execute("\killjob 2")
ms.execute("\killjob 3")

ms.execute("kill @e[type=minecraft:minecart]")
x, y, z = [int(p) for p in ms.player().position]

ms.execute(f"tp @p {x-26} {y-19} {z-15}")
ms.player_set_orientation(-90.0,0.0)