#!/usr/bin/env python3
"""randpick - Random selection, shuffling, and decision maker.

Single-file, zero-dependency CLI.
"""

import sys
import argparse
import random


def cmd_pick(args):
    items = args.items if args.items else [l.strip() for l in sys.stdin if l.strip()]
    if not items:
        print("  No items"); return 1
    r = random.Random(args.seed)
    picks = r.sample(items, min(args.count, len(items)))
    for p in picks:
        print(f"  🎯 {p}")


def cmd_shuffle(args):
    items = args.items if args.items else [l.strip() for l in sys.stdin if l.strip()]
    r = random.Random(args.seed)
    r.shuffle(items)
    for i, item in enumerate(items, 1):
        print(f"  {i:3d}. {item}")


def cmd_coin(args):
    r = random.Random(args.seed)
    results = [r.choice(["Heads", "Tails"]) for _ in range(args.count)]
    for res in results:
        emoji = "🪙" if res == "Heads" else "🔵"
        print(f"  {emoji} {res}")
    if args.count > 1:
        h = results.count("Heads")
        print(f"\n  Heads: {h}/{args.count} ({h/args.count*100:.0f}%)")


def cmd_dice(args):
    r = random.Random(args.seed)
    results = [r.randint(1, args.sides) for _ in range(args.count)]
    dice_emoji = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
    for res in results:
        emoji = dice_emoji.get(res, "🎲")
        print(f"  {emoji} {res}")
    if args.count > 1:
        print(f"\n  Total: {sum(results)}  Avg: {sum(results)/len(results):.1f}")


def cmd_number(args):
    r = random.Random(args.seed)
    for _ in range(args.count):
        print(f"  {r.randint(args.min, args.max)}")


def cmd_weighted(args):
    """Weighted random pick from key=weight pairs."""
    items = {}
    for pair in args.items:
        if "=" in pair:
            k, w = pair.rsplit("=", 1)
            items[k] = float(w)
        else:
            items[pair] = 1.0
    r = random.Random(args.seed)
    keys = list(items.keys())
    weights = [items[k] for k in keys]
    picks = r.choices(keys, weights=weights, k=args.count)
    for p in picks:
        print(f"  🎯 {p} (weight: {items[p]})")


def main():
    p = argparse.ArgumentParser(prog="randpick", description="Random selection tool")
    p.add_argument("-s", "--seed", type=int)
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("pick", help="Pick random items"); s.add_argument("items", nargs="*"); s.add_argument("-n", "--count", type=int, default=1)
    s = sub.add_parser("shuffle", help="Shuffle items"); s.add_argument("items", nargs="*")
    s = sub.add_parser("coin", help="Flip coin"); s.add_argument("-n", "--count", type=int, default=1)
    s = sub.add_parser("dice", help="Roll dice"); s.add_argument("-n", "--count", type=int, default=1); s.add_argument("--sides", type=int, default=6)
    s = sub.add_parser("number", aliases=["num"], help="Random number"); s.add_argument("min", type=int); s.add_argument("max", type=int); s.add_argument("-n", "--count", type=int, default=1)
    s = sub.add_parser("weighted", aliases=["w"], help="Weighted pick"); s.add_argument("items", nargs="+"); s.add_argument("-n", "--count", type=int, default=1)
    args = p.parse_args()
    if not args.cmd: p.print_help(); return 1
    cmds = {"pick": cmd_pick, "shuffle": cmd_shuffle, "coin": cmd_coin, "dice": cmd_dice,
            "number": cmd_number, "num": cmd_number, "weighted": cmd_weighted, "w": cmd_weighted}
    return cmds[args.cmd](args) or 0


if __name__ == "__main__":
    sys.exit(main())
