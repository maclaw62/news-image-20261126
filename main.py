"""Entry program: publish the prepared news board image.

The sandbox runs this file twice with no network and a read-only
repository, so it simply copies entry.png to /output/entry.png.
Copying fixed bytes keeps both runs identical.
"""

import shutil
from pathlib import Path


def publish():
    here = Path(__file__).resolve().parent
    target = Path("/output/entry.png")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(here / "entry.png", target)


if __name__ == "__main__":
    publish()
