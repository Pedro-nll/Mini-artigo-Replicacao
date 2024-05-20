import os
import pandas as pd

projects = ["public-apis", "stable-diffusion-webui", "youtube-dl", "transformers", "langchain", "pytorch"]
metrics = ["LOC", "NOM", "NOC", "CyclomaticComplexity"]

# Initialize an empty list to store the dataframes
dataframes = []

for project in projects:
    code_metrics_file = f"./metrics/{project}_code_metrics.csv"
    text_metrics_file = f"./metrics/{project}_test_metrics.csv"

    # Read the code metrics CSV file
    code_metrics_df = pd.read_csv(code_metrics_file)
    code_metrics_df["Project"] = project
    code_metrics_df["MetricType"] = "Code"

    # Read the text metrics CSV file
    text_metrics_df = pd.read_csv(text_metrics_file)
    text_metrics_df["Project"] = project
    text_metrics_df["MetricType"] = "Text"

    # Append the dataframes to the list
    dataframes.append(code_metrics_df)
    dataframes.append(text_metrics_df)

# Concatenate all the dataframes vertically
combined_df = pd.concat(dataframes, ignore_index=True)

# Reorder the columns
columns_order = ["Project", "MetricType", "Version"] + metrics
combined_df = combined_df[columns_order]

# Save the combined dataframe to a CSV file
output_file = "./combined_metrics.csv"
combined_df.to_csv(output_file, index=False)

print(f"Combined metrics saved to {output_file}")