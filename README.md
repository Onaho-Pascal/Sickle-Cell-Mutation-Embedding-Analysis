# 🧬 Sickle Cell Mutation Embedding Analysis (ESM2 Mini-Project)

**Author:** Pascal Onaho  
**Environment:** Python (conda), PyTorch, ESM2  

---

## 🧩 Background

The **E6V (Glu→Val)** substitution in the *β-globin* chain (HBB gene) is the defining mutation of **Sickle Cell Disease (SCD)**.  
It does **not** denature the β-globin structure but instead introduces a **hydrophobic patch** that promotes polymerization of hemoglobin molecules under low oxygen tension.

This mini-project explores how **sequence embeddings** from Meta’s **ESM-2** protein language model capture the subtle but biologically significant local effects of the E6V mutation without using full 3D folding models.

---

## ⚙️ Method

1. Retrieved the **wild-type (WT)** human HBB sequence from [UniProt: P68871](https://www.uniprot.org/uniprot/P68871).  
2. Generated a **mutant version (E6V)** by substituting glutamic acid (E) → valine (V) at position 6.  
3. Used the **ESM2-t6-8M** model to obtain residue-wise embeddings for both sequences.  
4. Computed:
   - **Cosine similarity** (for directional embedding similarity)  
   - **Euclidean distance** (for absolute embedding difference)  
   - **Residue-wise embedding distance curve**  
   - **Residue-wise cosine similarity heatmap**
5. Visualized and saved plots using Matplotlib and Seaborn.

---

## 📊 Results

| Metric | Value | Interpretation |
|--------|--------|----------------|
| **Cosine similarity** | **0.9996** | Almost identical global structure representation |
| **Euclidean distance** | **0.1572** | Small but meaningful local perturbation |

The residue-wise embedding curve showed a **sharp rise near residues 1–20**, peaking around **residue 6** — the known mutation site — before flattening across the rest of the sequence.  
This indicates a **localized disruption** in the learned sequence–structure embedding, while the overall fold remains stable.

The cosine similarity heatmap further confirms this:  
- Strong diagonal alignment (WT vs mutant) across most residues  
- Slight deviation around the N-terminal region, consistent with the **E6V site’s hydrophobic alteration**

---

## 🧠 Interpretation

- The **E6V mutation** triggers a **localized embedding shift** confined to the N-terminal region (around residue 6).  
- The rest of the β-globin remains structurally conserved in ESM2 embedding space.  
- This aligns with known experimental evidence: the mutation’s effect is **local** (hydrophobic exposure) rather than **global** (misfolding).  
- Hence, ESM2 captures **biologically relevant mutation signatures** even from pure sequence context.

---

## 📁 Output Files

| File | Description |
|------|--------------|
| `embedding_difference_curve.png` | Residue-wise embedding distance curve highlighting mutation impact |
| `embedding_heatmap.png` | Residue-level cosine similarity matrix between WT and E6V embeddings |

All results are saved in the `results/` folder.

---

## 🚀 Future Work

- Compare other clinically relevant variants (HbC, HbE, HbD).  
- Explore embeddings from larger ESM2 models (e.g., 650M parameters).  
- Integrate embeddings with **structural predictions** (OpenFold3) or **molecular dynamics** simulations for deeper validation.  
- Extend to multi-variant comparison and principal component clustering.

---

## 💡 Acknowledgements

This analysis uses **Meta’s ESM-2** model — a transformer-based protein language model that learns structural and functional context from raw amino acid sequences.  
Inspired by the long-standing biochemical insights into β-globin and the molecular basis of Sickle Cell Disease.

---

> “Even sequence alone can whisper the secrets of structure.” — Adapted from the AlphaFold philosophy
