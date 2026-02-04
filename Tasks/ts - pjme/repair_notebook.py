import nbformat

with open("Untitled.ipynb", "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

with open("Untitled-f.ipynb", "w", encoding="utf-8") as f:
    nbformat.write(nb, f)
