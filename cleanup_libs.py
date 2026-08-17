import os

libs_dir = r"extracted_plugin.video.palantir3\plugin.video.palantir3\libs"

for fname in os.listdir(libs_dir):
    if fname.endswith('.py') and fname != '__init__.py':
        fpath = os.path.join(libs_dir, fname)
        os.remove(fpath)
        print(f"Removed temporary {fname}")

print("Cleaned up libs folder!")
