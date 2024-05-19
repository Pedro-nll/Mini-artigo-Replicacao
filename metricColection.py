import os
import csv
import radon.raw
import radon.visitors
from radon.complexity import cc_visit
import chardet


def analyze_project(project_path, test_path):
    metrics = {"LOC": 0, "NOM": 0, "NOC": 0, "CyclomaticComplexity": 0}

    for version in range(1, 13):
        version_path = project_path + f"_version_{version}"
        test_version_path = os.path.join(version_path, test_path)
        loc = nom = noc = cc = 0

        print(f"Analyzing version {version} of the project...")

        for root, dirs, files in os.walk(version_path):
            if root.startswith(test_version_path):
                continue
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    print(f"Analyzing file: {file_path}")
                    try:
                        with open(file_path, "r") as f:
                            source = f.read()
                            module = radon.raw.analyze(source)
                            blocks = cc_visit(source)
                            loc += len(source.splitlines())
                            for node in blocks:
                                if node.__class__.__name__ == 'Function':
                                    nom += 1
                                if node.__class__.__name__ == 'Class':
                                    noc += 1
                            cc += radon.visitors.ComplexityVisitor.from_code(source).total_complexity
                    except SyntaxError as e:
                        print(f"SyntaxError in {file_path}: {e}")
                        continue
                    except UnicodeDecodeError as e:
                        print(f"UnicodeDecodeError in {file_path}: {e}")
                        continue

        metrics["LOC"] += loc
        metrics["NOM"] += nom
        metrics["NOC"] += noc
        metrics["CyclomaticComplexity"] += cc

    for metric in metrics:
        metrics[metric] /= 12  # Calculate the average over 12 versions

    return metrics

def analyze_tests(project_path, test_path):
    metrics = {"LOC": 0, "NOM": 0, "NOC": 0, "CyclomaticComplexity": 0}

    for version in range(1, 13):
        version_path = project_path + f"_version_{version}"
        test_version_path = os.path.join(version_path, test_path)
        loc = nom = noc = cc = 0

        print(f"Analyzing tests for version {version} of the project...")

        for root, dirs, files in os.walk(test_version_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    print(f"Analyzing test file: {file_path}")
                    with open(file_path, "r") as f:
                        source = f.read()
                        module = radon.raw.analyze(source)
                        blocks = cc_visit(source)
                        loc += len(source.splitlines())
                        for node in blocks:
                            if node.__class__.__name__ == 'Function':
                                nom += 1
                            if node.__class__.__name__ == 'Class':
                                noc += 1
                        cc += radon.visitors.ComplexityVisitor.from_code(source).total_complexity

        metrics["LOC"] += loc
        metrics["NOM"] += nom
        metrics["NOC"] += noc
        metrics["CyclomaticComplexity"] += cc

    for metric in metrics:
        metrics[metric] /= 12  # Calculate the average over 12 versions

    return metrics

# Test folder paths for each project
test_paths = {
    "public-apis": "./scripts/tests",
    "stable-diffusion-webui": "./test",
    "youtube-dl": "./test",
    "transformers": "./tests",
    "langchain": "./libs/core/tests",
    "pytorch": "./test"
}

repos = {
    "public-apis/public-apis": "https://github.com/public-apis/public-apis",
    "AUTOMATIC1111/stable-diffusion-webui": "https://github.com/AUTOMATIC1111/stable-diffusion-webui",
    "ytdl-org/youtube-dl": "https://github.com/ytdl-org/youtube-dl",
    "huggingface/transformers": "https://github.com/huggingface/transformers",
    "langchain-ai/langchain": "https://github.com/langchain-ai/langchain",
    "pytorch/pytorch": "https://github.com/pytorch/pytorch"
}

def main():
    # Create folders if they don't exist
    os.makedirs("./metrics", exist_ok=True)

    # Analyze each project
    for project, url in repos.items():
        project_name = project.split("/")[1]
        code_path = f"./repos/{project}"
        test_path = test_paths[project_name]
        
        code_metrics_csv_path = f"./metrics/{project_name}_code_metrics.csv"
        test_metrics_csv_path = f"./metrics/{project_name}_test_metrics.csv"

        # Skip project if CSV files already exist
        if os.path.exists(code_metrics_csv_path) and os.path.exists(test_metrics_csv_path):
            print(f"CSV files already exist for project: {project_name}. Skipping...")
            continue

        print(f"Analyzing code metrics for project: {project_name}")
        code_metrics = analyze_project(code_path, test_path)

        # Write code metrics to CSV
        with open(code_metrics_csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            for metric, value in code_metrics.items():
                writer.writerow([metric, value])

        print(f"Analyzing test metrics for project: {project_name}")
        test_metrics = analyze_tests(code_path, test_path)

        # Write test metrics to CSV
        with open(test_metrics_csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            for metric, value in test_metrics.items():
                writer.writerow([metric, value])

if __name__ == "__main__":
    main()
