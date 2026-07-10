import os

# Add your services here
services = [
    "service-a",
    "service-b"
]

results = []


def progress_bar(percent):
    """
    Returns a 10-block progress bar.
    Example:
    75% -> ████████░░
    """
    filled = int(round(percent / 10))
    return "█" * filled + "░" * (10 - filled)


for service in services:

    total_lines = 0
    ai_lines = 0

    for root, dirs, files in os.walk(service):

        for file in files:

            if not file.endswith(".java"):
                continue

            inside_ai = False

            path = os.path.join(root, file)

            with open(path, encoding="utf-8") as f:

                for line in f:

                    line = line.strip()

                    if not line:
                        continue

                    total_lines += 1

                    if "AI START" in line:
                        inside_ai = True
                        continue

                    if "AI END" in line:
                        inside_ai = False
                        continue

                    if inside_ai:
                        ai_lines += 1

    coverage = (
        round(ai_lines * 100 / total_lines, 2)
        if total_lines else 0
    )

    results.append(
        (service, total_lines, ai_lines, coverage)
    )

    print(f"{service} : {coverage}%")

#
# GitHub Workflow Summary
#

summary = os.getenv("GITHUB_STEP_SUMMARY")

if summary:

    overall_ai = 0
    overall_total = 0

    with open(summary, "w") as f:

        f.write("# 🤖 AI Generated Code Coverage\n\n")

        f.write("| Service | Coverage |\n")
        f.write("|:---------|:----------------------------|\n")

        for service, total, ai, coverage in results:

            overall_ai += ai
            overall_total += total

            bar = progress_bar(coverage)

            f.write(
                f"| **{service}** | {bar} **{coverage:.2f}%** |\n"
            )

        overall = (
            round(overall_ai * 100 / overall_total, 2)
            if overall_total else 0
        )

        f.write("\n---\n\n")

        f.write(
            f"## Overall AI Coverage : **{overall:.2f}%**\n"
        )

print("Completed Successfully")
