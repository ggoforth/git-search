#!/usr/bin/env python3
import os.path
import subprocess
import argparse
import datetime

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--start", required=True, help="Start date in format YYYY-MM-DD")
ap.add_argument("-e", "--end", required=True, help="End date in format YYYY-MM-DD")
ap.add_argument("-a", "--author", required=False, help="Author of the commits")
ap.add_argument("-o", "--output", required=False, help="directory path to output the commits file")
args = vars(ap.parse_args())

try:
    start = datetime.datetime.strptime(args["start"], "%Y-%m-%d").date()
    end = datetime.datetime.strptime(args["end"], "%Y-%m-%d").date()
except ValueError:
    raise ValueError("Incorrect data format, it should be YYYY-MM-DD")

subprocess.run(["git", "fetch", "--all"], check=True)

branches_proc = subprocess.run(["git", "branch", "-r"], check=True, text=True, stdout=subprocess.PIPE)
branches = branches_proc.stdout.splitlines()

branches = [branch.strip() for branch in branches if branch.strip().startswith("origin/") and "HEAD" not in branch]

commits = {}

for branch in branches:
    git_command = [
        "git",
        "log",
        "--no-merges",
        f"--since={start.isoformat()}",
        f"--until={end.isoformat()}",
        f"--author={args['author']}",
        "--pretty=format:%h ||| %an, %ad : %s",
        branch
    ]

    if args["author"] is None:
        git_command.remove(f"--author={args['author']}")

    result = subprocess.run(git_command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0 and result.stdout.strip() != "":
        branch_commits = result.stdout.strip().split("\n")
        for commit in branch_commits:
            commit_hash, commit_info = commit.split(" ||| ", 1)
            author, commit_date_and_desc = commit_info.split(", ", 1)
            commit_date, commit_desc = commit_date_and_desc.split(" : ", 1)
            commit_date = datetime.datetime.strptime(commit_date, '%a %b %d %H:%M:%S %Y %z')  # Adjust based on actual format.
            commits[commit_hash] = (author, commit_date, commit_desc, branch)

# Sort commits by date
sorted_commits = sorted(commits.items(), key=lambda x: x[1][1])  # Sorts based on date (second element of tuple)

output_path = os.path.expanduser(args.get("output"))
if output_path:
    file = f"{output_path}/{'' if not args['author'] else args['author'].lower() + '-'}commits.txt"
    with open(file, 'w') as file:
        for commit_hash, commit_info in sorted_commits:
            author, commit_date, commit_desc, branch = commit_info
            file.write(f"{commit_hash} | {author} | {commit_date} : {commit_desc}\n")
        file.write(f"Total commits found for the time period: {len(sorted_commits)}\n")
        print(f"Commits written to {file.name}")
else:
    for commit_hash, commit_info in sorted_commits:
        author, commit_date, commit_desc, branch = commit_info
        print(f"{commit_hash} | {author}, {commit_date} : {commit_desc}")
    print(f"Total commits found for the time period: {len(sorted_commits)}")






