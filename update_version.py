import re
import sys

def update_version_in_pyproject(version):
    path = "pyproject.toml"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(r'version\s*=\s*"[0-9\.]+"', f'version = "{version}"', content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_version.py <version>")
        sys.exit(1)
    version = sys.argv[1]
    update_version_in_pyproject(version)
