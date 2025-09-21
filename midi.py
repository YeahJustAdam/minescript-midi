import mido 
import minescript as ms
import time
import sys, os

DRUM_MAP = {
    35: "kick", 36: "kick",
    38: "snare", 40: "snare",
}

NB_MIN, NB_MAX = 54, 78  # rozsah noteblocků v MIDI číslech

def run_with_listener(x, y, z, events):
    # start listener in background
    ms.execute("\listen")
    ms.execute(r"\align")
    time.sleep(1)  # wait a bit for listener to start
    tp_string = f"tp @p {x+25} {y+21} {z+15}"
    ms.player_set_orientation(180, 90)
    ms.execute(tp_string)
    ms.chat("Track spawned! Now run the midi_to_noteblocks function with your MIDI file path.")
    # now do your MIDI playback
    spawn_minecarts_from_events(x, y, z, events, lead_time=0.5, tick_ms=10)

def fold_octave(note: int) -> int:
    """Moves notes into the range of NB_MIN..NB_MAX by shifting octaves."""
    while note < NB_MIN:
        note += 12
    while note > NB_MAX:
        note -= 12
    return note

def midi_to_noteblocks(midi_file, speed=1.0):
    mid = mido.MidiFile(midi_file)
    tpb = mid.ticks_per_beat
    tempo = 500000 / speed # default 120 BPM
    events = []

    for track in mid.tracks:
        t_ticks = 0
        cur_tempo = tempo
        t_sec = 0.0
        for msg in track:
            if msg.time:
                t_sec += mido.tick2second(msg.time, tpb, cur_tempo)
            if msg.type == "set_tempo":
                cur_tempo = msg.tempo / speed
            elif msg.type == "note_on" and msg.velocity > 0:
                if getattr(msg, "channel", 0) == 9:
                    drum = DRUM_MAP.get(msg.note)
                    if drum:
                        events.append((t_sec, None, msg.velocity, drum))
                else:
                    n_map = fold_octave(msg.note)
                    idx = n_map - NB_MIN
                    events.append((t_sec, idx, msg.velocity, None))
    events.sort(key=lambda e: e[0])
    return events




def spawn_minecarts(x, y, z):
    """ Spawn minecarts at specified coordinates based on which notes should be played. """
    for i in range(0, 25):
        summon_str = f"summon minecraft:minecart {x} {y+1} {z+i} {{Motion:[0.5,0.0,0.0]}}"
        ms.execute(summon_str)


def spawn_track():
    """ Spawn a track with note blocks on which the song will be played. """
    x, y, z = [int(p) for p in ms.player().position]
    x = x + 1
    fill_str_red = f"fill {x} {y} {z} {x+50} {y} {z+35} minecraft:redstone_block"
    fill_str_rail = f"fill {x} {y+1} {z} {x+50} {y+1} {z+35} minecraft:powered_rail[shape=east_west]"
    fill_str_wool = f"fill {x+25} {y+2} {z} {x+25} {y+2} {z+35} minecraft:glowstone"
    for i in range(0, 25):
        setblock_str_noteblock = f"setblock {x+25} {y+3} {z+i} minecraft:note_block[note={i}]"
        ms.execute(setblock_str_noteblock)
    setblock_str_bass = f"setblock {x+25} {y+3} {z+26} minecraft:note_block"
    setblock_str_snare = f"setblock {x+25} {y+3} {z+27} minecraft:note_block[note=20]"
    setblock_str_under_bass = f"setblock {x+25} {y+2} {z+26} minecraft:stone"
    setblock_str_under_snare = f"setblock {x+25} {y+2} {z+27} minecraft:sand"
    ms.execute(fill_str_red)
    ms.execute(fill_str_rail)
    ms.execute(fill_str_wool)
    ms.execute(setblock_str_bass)
    ms.execute(setblock_str_snare)
    ms.execute(setblock_str_under_bass)
    ms.execute(setblock_str_under_snare)
    ms.execute(f"setblock {x+25} {y+20} {z+15} minecraft:glass")


    # return the starting coordinates of the track
    return x, y, z

def spawn_minecarts_from_events(x, y, z, events, lead_time=0.5, tick_ms=10):
    """
    Spustí minecarty podle fronty `events`.
    - x,y,z: začátek tvého tracku (z returnu spawn_track())
    - events: [(time_sec, note_index, velocity, drum)]
        drum = "kick"/"snare"/None
    - lead_time: kolik sekund počkat než to začne (ať se stihneš připravit)
    - tick_ms: jemnost smyčky (ms)
    """
    ms.chat(f"Začínám přehrávat za {lead_time:.1f}s. Událostí: {len(events)}")
    time.sleep(lead_time)
    t0 = time.perf_counter()
    i = 0
    while i < len(events):
        now = time.perf_counter() - t0
        t, idx, vel, drum = events[i]
        if now + tick_ms/1000.0 >= t:
            vx = 0.35 + 0.45 * (vel / 127.0)

            if drum == "kick":
                summon_str = (
                    f"summon minecraft:minecart {x} {y+1} {z+26} "
                    f"{{Motion:[{vx:.3f},0.0,0.0]}}"
                )
            elif drum == "snare":
                summon_str = (
                    f"summon minecraft:minecart {x} {y+1} {z+27} "
                    f"{{Motion:[{vx:.3f},0.0,0.0]}}"
                )
            else:
                summon_str = (
                    f"summon minecraft:minecart {x} {y+1} {z+idx} "
                    f"{{Motion:[{vx:.3f},0.0,0.0]}}"
                )

            ms.execute(summon_str)
            i += 1
        #else:
            #time.sleep(tick_ms/1000.0)



if __name__ == "__main__":
    args = sys.argv[1]
    if not args:
        ms.chat("Usage: \midi list")
        ms.chat("Usage: \midi <midi_file_path>")
        sys.exit(1)
    if args == "list":
        ms.chat("Available MIDI files in 'midis' folder:")
        midis_path = os.path.join(os.path.dirname(__file__), "midis")
        for f in os.listdir(midis_path):
            if f.lower().endswith(".mid") or f.lower().endswith(".midi"):
                ms.chat(f"- {f}")
        sys.exit(0)
    if sys.argv[2]:
        speed = float(sys.argv[2])
        if speed <= 0.0:
            speed = 1.0
        elif speed > 10.0:
            speed = 10.0
    else:
        speed = 1.0
    
    midi_file_path = os.path.join(os.path.dirname(__file__), "midis", args)
    if not os.path.isfile(midi_file_path):
        sys.exit(1)
    
    ms.chat("starting midi")
    x,y,z = spawn_track()
    events = midi_to_noteblocks(midi_file_path, speed)
    run_with_listener(x, y, z, events)
    ms.execute("\stop_midi")