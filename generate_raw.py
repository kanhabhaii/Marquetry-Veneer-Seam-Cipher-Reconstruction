from pathlib import Path
import random

import pandas as pd


N_PACKETS = 960
LEAVES_PER_PACKET = 8
SEED = 714923

BOUNDARY_COUNT = 88
LEFT_CODES = [f"LX{idx:02d}{suffix}" for idx, suffix in enumerate(
    ["amber", "bistre", "cedar", "drift", "elm", "flax", "gesso", "hazel"] * 11
)]
RIGHT_CODES = [f"RQ{idx:02d}{suffix}" for idx, suffix in enumerate(
    ["ivory", "juniper", "kermes", "lichen", "madder", "nacre", "ochre", "pewter"] * 11
)]
START_LEFT_CODES = ["START_ASTER", "START_BEECH", "START_CLOVE", "START_DAMAR"]
END_RIGHT_CODES = ["END_EBONY", "END_FERN", "END_GILDER", "END_HOLLY"]
WOOD_SPECIES = ["walnut", "maple", "pearwood", "rosewood", "satinwood", "elm burl"]
FIGURE_WORDS = ["curl", "ray", "flame", "mottle", "stripe", "birdseye", "ripple", "fiddleback"]
WAX_MARKS = ["blue", "red", "white", "black", "green", "yellow"]


def _choose_unique(rng, values, count):
    return rng.sample(values, count)


def _leaf_id(rng, packet_index, leaf_index):
    alphabet = "BDEFGHJKLMNPQSTUVWXYZ23456789"
    suffix = "".join(rng.choice(alphabet) for _ in range(5))
    return f"rawleaf_{packet_index:04d}_{leaf_index}_{suffix}"


def _make_leaf_record(leaf_id, left_sig, right_sig, rng):
    species = rng.choice(WOOD_SPECIES)
    figure = rng.choice(FIGURE_WORDS)
    wax = rng.choice(WAX_MARKS)
    caliper = 17 + rng.randrange(12)
    pin = rng.randrange(10)
    return (
        f"{leaf_id}"
        f"~left:{left_sig}"
        f"~right:{right_sig}"
        f"~wood:{species}"
        f"~figure:{figure}"
        f"~wax:{wax}"
        f"~caliper:{caliper}"
        f"~pin:{pin}"
    )


def _make_packet(packet_index, rng):
    start_left = rng.choice(START_LEFT_CODES)
    end_right = rng.choice(END_RIGHT_CODES)
    internal_boundaries = _choose_unique(rng, list(range(BOUNDARY_COUNT)), LEAVES_PER_PACKET - 1)
    left_signatures = [start_left] + [LEFT_CODES[idx] for idx in internal_boundaries]
    right_signatures = [RIGHT_CODES[idx] for idx in internal_boundaries] + [end_right]

    leaf_ids = [_leaf_id(rng, packet_index, idx) for idx in range(LEAVES_PER_PACKET)]
    true_order = leaf_ids[:]
    records = [
        _make_leaf_record(leaf_ids[idx], left_signatures[idx], right_signatures[idx], rng)
        for idx in range(LEAVES_PER_PACKET)
    ]
    shuffled = records[:]
    rng.shuffle(shuffled)

    difficulty = rng.choices(["plain", "smudged", "busy"], weights=[35, 45, 20], k=1)[0]
    if difficulty in {"smudged", "busy"}:
        shuffled.append(
            f"shopnote~left:IGNORE_{rng.randrange(100):02d}~right:IGNORE_{rng.randrange(100):02d}"
            f"~wood:scrap~figure:practice~wax:none~caliper:0~pin:0"
        )
    if difficulty == "busy":
        shuffled.append(
            f"guardstrip~left:GUARD_{rng.randrange(100):02d}~right:GUARD_{rng.randrange(100):02d}"
            f"~wood:paper~figure:separator~wax:none~caliper:0~pin:0"
        )
    rng.shuffle(shuffled)

    return {
        "packet_id": f"veneer_packet_{packet_index:05d}",
        "piece_catalog_raw": " || ".join(shuffled),
        "leaf_order_raw": "|".join(true_order),
        "leaf_count": LEAVES_PER_PACKET,
        "difficulty": difficulty,
        "start_left_raw": start_left,
        "end_right_raw": end_right,
        "boundary_indices": "|".join(str(idx) for idx in internal_boundaries),
    }


def main():
    root = Path(__file__).resolve().parent
    rng = random.Random(SEED)
    rows = [_make_packet(idx, rng) for idx in range(N_PACKETS)]
    pd.DataFrame(rows).to_csv(root / "data.csv", index=False)
    print(f"wrote {len(rows)} packets to {root}")


if __name__ == "__main__":
    main()
