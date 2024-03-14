# Git Commit Explorer

This Python script allows you to explore and output Git commits based on a provided date range and optionally by the author of the commits.

Before using, make sure to have Python 3 installed on your machine.

## Installation

No additional installation is required. Copy the `git_commit_explorer.py` script to your local machine and run it from your command line.

## Usage

`git_search.py -s START_DATE -e END_DATE [-a AUTHOR] [-o OUTPUT]`

_Note:_ The script needs to be run from within a git repository.

## Arguments

Here is what each argument signifies:

-   `-s` or `--start` : **(Mandatory)** The start date (inclusive) of the period within which you want to retrieve the commits. Format should be `YYYY-MM-DD`.

-   `-e` or `--end` : **(Mandatory)** The end date (inclusive) of the period within which you want to retrieve the commits. Format should be `YYYY-MM-DD`.

-   `-a` or `--author` : **(Optional)** If specified, the script will fetch commits made by the given author. If not specified, commits made by all authors will be fetched.

-   `-o` or `--output` : **(Optional)** If specified, the script will write the commits in a file in the given directory. The filename will be `commits.txt` or `<author>-commits.txt` if the author's name is provided.

## Output

For each commit, the following information will be output:

1. Commit hash
2. Author name
3. Commit date and time
4. Commit message

In the end, the total number of commits found for the given period and author will be displayed.

## Error Handling

The script validates the date input formats. If the input is not in the correct form of `YYYY-MM-DD`, the script will stop execution and show an error message.

## Feedback

For any bugs or enhancements, feel free to open an issue on this repository.