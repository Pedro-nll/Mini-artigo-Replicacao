import pandas as pd
import matplotlib.pyplot as plt

projects = ["public-apis", "stable-diffusion-webui", "youtube-dl", "transformers", "langchain", "pytorch"]
metrics = ["LOC", "NOM", "NOC", "CyclomaticComplexity"]

def annotate_points(ax, x_values, y_values):
    if len(x_values) > 0:
        middle_idx = len(x_values) // 2
        end_idx = len(x_values) - 1

        if len(x_values) > 1:
            ax.annotate(f'{y_values[middle_idx]}', xy=(x_values[middle_idx], y_values[middle_idx]), 
                        xytext=(0, 5), textcoords='offset points', ha='center', fontsize=8)

        ax.annotate(f'{y_values[end_idx]}', xy=(x_values[end_idx], y_values[end_idx]), 
                    xytext=(0, 5), textcoords='offset points', ha='center', fontsize=8)

# RQ1: NOM, NOC, LOC
for metric in ["LOC", "NOM", "NOC"]:
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    for idx, project in enumerate(projects):
        row, col = divmod(idx, 3)
        code_metrics = pd.read_csv(f'./metrics/{project}_code_metrics.csv')
        test_metrics = pd.read_csv(f'./metrics/{project}_test_metrics.csv')

        ax = axes[row, col]
        ax.plot(code_metrics['Version'], code_metrics[metric], label='Code')
        ax.plot(test_metrics['Version'], test_metrics[metric], label='Test', linestyle='--')

        annotate_points(ax, code_metrics['Version'], code_metrics[metric])
        annotate_points(ax, test_metrics['Version'], test_metrics[metric])

        ax.set_title(f'{project}')
        ax.set_xlabel('Version')
        ax.set_ylabel(metric)
        ax.legend()

    plt.suptitle(f'{metric} Over Versions for All Projects')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'./plots/all_projects_{metric}.png')
    plt.close()

# RQ2: Cyclomatic Complexity
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
for idx, project in enumerate(projects):
    row, col = divmod(idx, 3)
    code_metrics = pd.read_csv(f'./metrics/{project}_code_metrics.csv')
    test_metrics = pd.read_csv(f'./metrics/{project}_test_metrics.csv')

    ax = axes[row, col]
    ax.plot(code_metrics['Version'], code_metrics['CyclomaticComplexity'], label='Code')
    ax.plot(test_metrics['Version'], test_metrics['CyclomaticComplexity'], label='Test', linestyle='--')

    annotate_points(ax, code_metrics['Version'], code_metrics['CyclomaticComplexity'])
    annotate_points(ax, test_metrics['Version'], test_metrics['CyclomaticComplexity'])

    ax.set_title(f'{project}')
    ax.set_xlabel('Version')
    ax.set_ylabel('Cyclomatic Complexity')
    ax.legend()

plt.suptitle('Cyclomatic Complexity Over Versions for All Projects')
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(f'./plots/all_projects_CyclomaticComplexity.png')
plt.close()
