"""Oracle for Árapály — students never see this module."""

from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def parse_arapaly(content: str) -> list[Row]:
    lines = _nonempty_lines(content)
    n, m = (int(x) for x in lines[0].split()[:2])
    grid = [[int(x) for x in line.split()] for line in lines[1 : 1 + n]]
    rows: list[Row] = []
    for i in range(n):
        for j in range(m):
            rows.append(
                {
                    "index": i * m + j + 1,
                    "row": i + 1,
                    "col": j + 1,
                    "depth": grid[i][j],
                    "n": n,
                    "m": m,
                    "grid": grid,
                }
            )
    return rows


def parse(content: str) -> list[Row]:
    return parse_arapaly(content)


def _grid(rows: list[Row]) -> tuple[int, int, list[list[int]]]:
    n = int(rows[0]["n"])
    m = int(rows[0]["m"])
    return n, m, rows[0]["grid"]


def _neighbors(grid: list[list[int]], i: int, j: int) -> dict[str, int]:
    n, m = len(grid), len(grid[0])
    out: dict[str, int] = {}
    if i > 0:
        out["N"] = grid[i - 1][j]
    if i + 1 < n:
        out["S"] = grid[i + 1][j]
    if j > 0:
        out["NY"] = grid[i][j - 1]
    if j + 1 < m:
        out["K"] = grid[i][j + 1]
    return out


def _basins(grid: list[list[int]]) -> list[tuple[int, int, int]]:
    found: list[tuple[int, int, int]] = []
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            nbs = _neighbors(grid, i, j)
            if nbs and all(val < v for v in nbs.values()):
                found.append((i + 1, j + 1, val))
    return found


def _task_arapaly_stats(rows: list[Row], _spec: dict[str, Any]) -> str:
    depths = [int(r["depth"]) for r in rows]
    return (
        f"A racspontok szama: {len(rows)}\n"
        f"A legkisebb melyseg: {min(depths)} cm\n"
        f"A legnagyobb melyseg: {max(depths)} cm"
    )


def _task_arapaly_medence(rows: list[Row], _spec: dict[str, Any]) -> str:
    _n, _m, grid = _grid(rows)
    return f"A medencek szama: {len(_basins(grid))}"


def _task_arapaly_cella(rows: list[Row], spec: dict[str, Any]) -> str:
    tokens = str(spec.get("stdin") or "1 1").split()
    sr, sc = int(tokens[0]), int(tokens[1])
    _n, _m, grid = _grid(rows)
    val = grid[sr - 1][sc - 1]
    nbs = _neighbors(grid, sr - 1, sc - 1)
    lines = [f"Sor:\nOszlop:\nA cella melysege: {val} cm"]
    for key in ("N", "S", "NY", "K"):
        if key in nbs:
            lines.append(f"{key}: {nbs[key]}")
    return "\n".join(lines)


def _task_arapaly_file(rows: list[Row], _spec: dict[str, Any]) -> str:
    _n, _m, grid = _grid(rows)
    return "\n".join(f"{r} {c} {d}" for r, c, d in _basins(grid))


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "arapaly_stats": _task_arapaly_stats,
    "arapaly_medence": _task_arapaly_medence,
    "arapaly_cella": _task_arapaly_cella,
    "arapaly_file": _task_arapaly_file,
}
