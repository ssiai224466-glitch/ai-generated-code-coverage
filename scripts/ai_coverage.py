import os

services = ["service-a", "service-b"]

results = []

for service in services:

    total = 0
    ai = 0

    for root, dirs, files in os.walk(service):

        for file in files:

            if not file.endswith(".java"):
                continue

            inside_ai = False

            with open(os.path.join(root, file), encoding="utf-8") as f:

                for line in f:

                    line = line.strip()

                    if not line:
                        continue

                    total += 1

                    if "AI START" in line:
                        inside_ai = True
                        continue

                    if "AI END" in line:
                        inside_ai = False
                        continue

                    if inside_ai:
                        ai += 1

    coverage = round(ai * 100 / total, 2)

    results.append((service, total, ai, coverage))

    print(f"{service} : {coverage}%")

#
# Write GitHub Summary
#

summary = os.getenv("GITHUB_STEP_SUMMARY")

if summary:

    with open(summary, "a") as f:

        f.write("# AI Generated Code Coverage\n\n")

        f.write("| Service | AI Lines | Total Lines | Coverage |\n")
        f.write("|---------|---------:|------------:|---------:|\n")

        for service, total, ai, coverage in results:

            f.write(
                f"| {service} | {ai} | {total} | **{coverage}%** |\n"
            )
