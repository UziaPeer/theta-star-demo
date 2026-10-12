"""Flask demo for Theta*: Any-Angle Path Planning on Grids (Nash et al., 2007).

Paper: https://cdn.aaai.org/AAAI/2007/AAAI07-187.pdf
Programmer: Uzia Peer. Date: 2026-10-12.
"""

import io
import logging
import os
from random import Random
from threading import Lock
from time import perf_counter

import networkx as nx
from flask import Flask, render_template, request

from networkz import CornerGrid, path_length, theta_star

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50_000
log_lock = Lock()
DEFAULT = "0 0 0 0 0\n0 1 1 0 0\n0 0 0 0 0\n0 0 1 0 0\n0 0 0 0 0"
PAPER = "https://cdn.aaai.org/AAAI/2007/AAAI07-187.pdf"


def parse_grid(text):
    rows = text.strip().splitlines()
    if not rows or len(rows) > 50:
        raise ValueError("יש להזין בין 1 ל־50 שורות.")
    cells = []
    for row in rows:
        values = row.split()
        if not 1 <= len(values) <= 50 or any(v not in ("0", "1") for v in values):
            raise ValueError("בכל שורה יש להזין עד 50 ערכי 0 או 1, מופרדים ברווחים.")
        cells.append([int(v) for v in values])
    if any(len(row) != len(cells[0]) for row in cells):
        raise ValueError("כל השורות בגריד חייבות להכיל אותו מספר תאים.")
    return CornerGrid(cells)


def point(form, prefix):
    try:
        return int(form[prefix + "x"]), int(form[prefix + "y"])
    except (KeyError, ValueError):
        raise ValueError(
            "קואורדינטות ההתחלה והיעד חייבות להיות מספרים שלמים."
        ) from None


@app.route("/", methods=["GET", "POST"])
def index():
    values = dict(
        cells=DEFAULT,
        sx=0,
        sy=0,
        gx=5,
        gy=5,
        variant="basic",
        width=5,
        height=5,
        density=20,
        seed=7,
    )
    if request.method == "POST":
        values.update(request.form)
        try:
            if request.form.get("action") == "random":
                width, height = int(values["width"]), int(values["height"])
                density, seed = int(values["density"]), int(values["seed"])
                if not (1 <= width <= 50 and 1 <= height <= 50 and 0 <= density <= 60):
                    raise ValueError("גודל הגריד חייב להיות 1–50 ואחוז החסימה 0–60.")
                rng = Random(seed)
                cells = [
                    [int(rng.random() < density / 100) for _ in range(width)]
                    for _ in range(height)
                ]
                cells[0][0] = cells[-1][-1] = 0
                values.update(
                    cells="\n".join(" ".join(map(str, r)) for r in cells),
                    sx=0,
                    sy=0,
                    gx=width,
                    gy=height,
                )
            else:
                grid = parse_grid(values["cells"])
                start, goal = point(values, "s"), point(values, "g")
                if not grid.valid_vertex(start) or not grid.valid_vertex(goal):
                    raise ValueError(
                        "נקודות ההתחלה והיעד חייבות להיות פינות בתוך הגריד, הנוגעות בתא פנוי."
                    )
                if values["variant"] not in ("basic", "ap"):
                    raise ValueError("בחרו Basic Theta* או AP Theta*.")
                output, stats, error = io.StringIO(), {}, None
                handler = logging.StreamHandler(output)
                handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
                algorithm_logger = logging.getLogger("networkz.algorithms.theta_star")
                # Logger configuration is shared: serialize capture, then restore it.
                with log_lock:
                    previous = algorithm_logger.level
                    algorithm_logger.setLevel(logging.DEBUG)
                    algorithm_logger.addHandler(handler)
                    t0 = perf_counter()
                    try:
                        path = theta_star(
                            grid,
                            start,
                            goal,
                            variant=values["variant"],
                            statistics=stats,
                        )
                    except nx.NetworkXNoPath:
                        path, error = [], "אין מסלול בין נקודת ההתחלה ליעד בגריד הזה."
                    finally:
                        runtime = perf_counter() - t0
                        algorithm_logger.removeHandler(handler)
                        algorithm_logger.setLevel(previous)
                segments = [
                    (a, b, grid.line_of_sight(a, b), path_length([a, b]))
                    for a, b in zip(path, path[1:])
                ]
                return render_template(
                    "result.html",
                    grid=grid,
                    path=path,
                    start=start,
                    goal=goal,
                    length=path_length(path),
                    runtime=runtime,
                    logs=output.getvalue(),
                    segments=segments,
                    stats=stats,
                    error=error,
                    values=values,
                    paper=PAPER,
                )
        except (ValueError, TypeError) as exc:
            return render_template(
                "index.html", values=values, error=str(exc), paper=PAPER
            ), 400
    return render_template("index.html", values=values, paper=PAPER)


@app.get("/about")
def about():
    return render_template(
        "about.html",
        author=os.environ.get("PROJECT_AUTHOR", "Uzia Peer"),
        paper=PAPER,
    )


@app.errorhandler(413)
def too_large(_error):
    return "הקלט גדול מדי. הגריד מוגבל ל־50×50 תאים.", 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
