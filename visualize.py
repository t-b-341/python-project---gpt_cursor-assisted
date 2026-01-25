# visualize.py
# - Saves plots as PNGs into telemetry_plots/
# - Shows a SINGLE popup window that pages through plots (n/p or arrows)
# - Press 'q' (or Esc) to close the window and end the program
# - Optional prompts: data from most recent run vs all runs; which plots to show

import argparse
import sqlite3

from telemetry_viz.core import get_pages, get_pages_all_runs
from telemetry_viz.db_utils import get_latest_run_id
from telemetry_viz.viewer import save_pngs, run_single_popup

DB_PATH_DEFAULT = "game_telemetry.db"
OUT_DIR_DEFAULT = "telemetry_plots"
SHOW_POPUP_DEFAULT = True


def _prompt_data_scope() -> str:
    """Ask: most recent run (1) or all runs (2). Returns '1' or '2'."""
    try:
        s = input("Data from: [1] most recent run  [2] all runs — choice (1/2) [1]: ").strip() or "1"
        return "2" if s == "2" else "1"
    except (EOFError, KeyboardInterrupt):
        return "1"


def _prompt_which_plots(all_pages: list) -> list:
    """Ask which plots to show. Returns list of Page (subset or all)."""
    n = len(all_pages)
    print("\nPlots (by number):")
    for i, p in enumerate(all_pages, 1):
        print(f"  {i:2}. {p.title}")
    try:
        raw = input(f"Which to show? ('all' or comma-separated 1–{n}) [all]: ").strip().lower() or "all"
    except (EOFError, KeyboardInterrupt):
        return all_pages

    if raw == "all":
        return all_pages

    chosen = []
    for part in raw.replace(" ", "").split(","):
        part = part.strip()
        if not part:
            continue
        try:
            idx = int(part)
            if 1 <= idx <= n:
                chosen.append(all_pages[idx - 1])
        except ValueError:
            continue
    return chosen if chosen else all_pages


def main() -> None:
    parser = argparse.ArgumentParser(description="Telemetry viz: save PNGs and/or show interactive viewer.")
    parser.add_argument("--db", default=DB_PATH_DEFAULT, help=f"SQLite database path (default: {DB_PATH_DEFAULT})")
    parser.add_argument("--out-dir", default=OUT_DIR_DEFAULT, help=f"Output directory for PNGs (default: {OUT_DIR_DEFAULT})")
    parser.add_argument("--no-popup", action="store_true", help="Do not show the interactive viewer after saving PNGs")
    parser.add_argument("--run-id", type=int, default=None, help="Use this run_id; default is latest run in DB")
    parser.add_argument("--no-prompts", action="store_true", help="Skip interactive prompts; use latest run and all plots")
    args = parser.parse_args()

    with sqlite3.connect(args.db) as conn:
        run_id = args.run_id if args.run_id is not None else get_latest_run_id(conn)
        if run_id is None:
            print("No runs found in the database.")
            return

        if args.no_prompts:
            pages = get_pages()
        else:
            scope = _prompt_data_scope()
            pages = get_pages_all_runs() if scope == "2" else get_pages()
            if scope == "2":
                print("Using plots that aggregate over all runs.")
            pages = _prompt_which_plots(pages)

        print(f"Using run_id={run_id} ({len(pages)} plot(s))")
        save_pngs(conn, run_id, pages, out_dir=args.out_dir)

        if not args.no_popup and SHOW_POPUP_DEFAULT:
            print("\nSingle popup controls: n/right=next, p/left=prev, q/esc=quit")
            run_single_popup(conn, run_id, pages)


if __name__ == "__main__":
    main()
