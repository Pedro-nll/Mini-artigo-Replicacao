import os
import pandas as pd
import matplotlib.pyplot as plt

projects = ["public-apis", "stable-diffusion-webui", "youtube-dl", "transformers", "langchain", "pytorch"]
metrics = ["LOC", "NOM", "NOC", "CyclomaticComplexity"]

def read_csv(project, metric_type):
    file_path = f"./metrics/{project}_{metric_type}_metrics.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return None

def average_data(df):
    return df.mean().tolist()

fig, axs = plt.subplots(2, 3, figsize=(12, 8))
axs = axs.flatten()

for i, project in enumerate(projects):
    code_df = read_csv(project, "code")
    text_df = read_csv(project, "test")

    if code_df is not None and text_df is not None:
        code_data = average_data(code_df[metrics])
        text_data = average_data(text_df[metrics])

        x = range(len(metrics))
        axs[i].bar([j - 0.2 for j in x], code_data, width=0.4, label="Code")
        axs[i].bar([j + 0.2 for j in x], text_data, width=0.4, label="Text")
        axs[i].set_xticks(x)
        axs[i].set_xticklabels(metrics, rotation=45)
        axs[i].set_title(project)
        axs[i].legend()

plt.tight_layout()
plt.show()