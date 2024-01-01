#!/usr/bin/env python3.12
import argparse
import shutil
import subprocess
from pathlib import Path


def replace_placeholder(path: Path, placeholder: str, value: str) -> None:
    if path.stem == placeholder:
        previous_path = path
        path = path.with_stem(value)
        shutil.move(previous_path, path)

    if not path.is_file():
        return

    with path.open() as f:
        new_content = f.read().replace(placeholder, value)
    with path.open("w") as f:
        f.write(new_content)


def generate(source: Path, dest: Path, placeholder: str, value: str) -> None:
    shutil.copytree(source, dest)

    for path in dest.rglob("*"):
        replace_placeholder(path, placeholder, value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", type=str)
    parser.add_argument("--out-dir", type=Path, default=Path.home() / "code")
    args = parser.parse_args()
    project_name: str = args.project_name
    out_dir: Path = args.out_dir
    dest = out_dir / project_name

    generate(
        source=Path(__file__).parent / "template",
        dest=dest,
        placeholder="REPLACE_PROJECT_NAME",
        value=project_name,
    )
    subprocess.check_call(("nvim", str(dest)))


if __name__ == "__main__":
    main()
