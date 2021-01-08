import os
import sys

src_path = os.path.join(os.path.dirname(__file__), "..", "src")
src_path = os.path.abspath(src_path)

sys.path.append(src_path)

from h_snippet import delete_gists

if __name__ == "__main__":
    sys.exit(delete_gists.run())
