"""
Sickle Cell Variant Embedding Analysis using ESM-2
-------------------------------------------------
Compares WT vs E6V mutant of human beta-globin using ESM2 embeddings.
Generates residue-wise embedding distance plot and heatmap.
"""

import torch
import esm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
import os

# ========== Configuration ==========
WT_SEQ = "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH"
MUT_SEQ = "MVHLTPVEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH"


OUT_DIR = "results"
os.makedirs(OUT_DIR, exist_ok=True)

print("Loading ESM-2 model...")
model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
batch_converter = alphabet.get_batch_converter()
model.eval()

# ========== Embed sequences ==========
data = [("WT", WT_SEQ), ("E6V", MUT_SEQ)]
batch_labels, batch_strs, batch_tokens = batch_converter(data)
with torch.no_grad():
    results = model(batch_tokens, repr_layers=[6], return_contacts=False)
embeddings = results["representations"][6]

# Mean-pool across residues
wt_embed = embeddings[0].mean(0)
mut_embed = embeddings[1].mean(0)

cos_sim = cosine_similarity(
    wt_embed.unsqueeze(0), mut_embed.unsqueeze(0)
)[0][0]
euclidean = torch.norm(wt_embed - mut_embed).item()

print(f"Cosine similarity (WT vs E6V): {cos_sim:.4f}")
print(f"Euclidean distance (embedding difference): {euclidean:.4f}")

# ========== Residue-wise difference ==========
wt_res = embeddings[0][1:len(WT_SEQ)+1]
mut_res = embeddings[1][1:len(MUT_SEQ)+1]
diff = torch.norm(wt_res - mut_res, dim=1).numpy()

# Plot: residue-wise embedding difference
plt.figure(figsize=(10,5))
plt.plot(np.arange(1, len(diff)+1), diff, color="royalblue")
plt.axvline(6, color="red", linestyle="--", label="E6V site")
plt.xlabel("Residue position")
plt.ylabel("Embedding distance (WT vs E6V)")
plt.title("Residue-wise ESM2 Embedding Difference - HBB (E6V)")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "embedding_difference_curve.png"), dpi=300)
plt.close()

# ========== Heatmap ==========
dist_matrix = cosine_similarity(wt_res, mut_res)
plt.figure(figsize=(8,6))
sns.heatmap(dist_matrix, cmap="viridis", vmin=0.95, vmax=1.0)
plt.title("Residue-wise Cosine Similarity Heatmap (WT vs E6V)")
plt.xlabel("Mutant residue index")
plt.ylabel("WT residue index")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "embedding_heatmap.png"), dpi=300)
plt.close()

print(f"✅ Figures saved to: {os.path.abspath(OUT_DIR)}")
