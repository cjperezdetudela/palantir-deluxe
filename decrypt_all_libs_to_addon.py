import base64
import os
import sys

def decrypt_md_content(data_bytes):
    length = len(data_bytes)
    third = length // 3
    
    part3 = data_bytes[length - third:]
    part1 = data_bytes[:third]
    part2_rev = data_bytes[third:length - third][::-1]
    
    reconstructed_b64 = part3 + part1 + part2_rev
    
    rem = len(reconstructed_b64) % 4
    if rem > 0:
        reconstructed_b64 += b'=' * (4 - rem)
        
    return base64.b64decode(reconstructed_b64).decode('utf-8', errors='ignore')

libs_dir = r"extracted_plugin.video.palantir3\plugin.video.palantir3\libs"

for fname in os.listdir(libs_dir):
    if fname.endswith('.md'):
        fpath = os.path.join(libs_dir, fname)
        with open(fpath, 'rb') as f:
            raw = f.read()
        try:
            decrypted = decrypt_md_content(raw)
            out_fname = fname.replace('.md', '.py')
            out_fpath = os.path.join(libs_dir, out_fname)
            with open(out_fpath, 'w', encoding='utf-8') as out_f:
                out_f.write(decrypted)
            print(f"Decrypted {fname} -> {out_fname} ({len(decrypted)} bytes)")
        except Exception as e:
            print(f"Failed to decrypt {fname}: {e}")

print("All libs decrypted and saved as .py modules!")
