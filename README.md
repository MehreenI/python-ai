# GitHub Profile CLI

A small command-line tool that fetches public GitHub profiles and saves them as JSON and CSV.

For each username you enter, it saves:

- `login`
- `name`
- `public_repos`
- `followers`

## Setup

You need Python 3.9 or newer.

1. **Create a virtual environment**

   ```bash
   python -m venv .venv
   ```

2. **Activate it**

   ```bash
 
   .venv\Scripts\Activate.ps1

   ```

3. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** by copying `.example.env`:

   ```bash
   copy .example.env .env
   ```

   | Variable | Required | Description |
   |---|---|---|
   | `API_ENDPOINT` | No | GitHub users API URL. Defaults to `https://api.github.com/users/` |
   | `GITHUB_TOKEN` | No | A GitHub personal access token. Without one, GitHub allows only 60 requests per hour. |
   | `MAX_RETRIES` | No | How many times to try a failed request. Defaults to `3` |
   | `RETRY_DELAY` | No | Seconds to wait between attempts. Defaults to `2` |
   | `TIMEOUT` | No | Seconds to wait for GitHub to respond. Defaults to `10` |
   | `OUTPUT_DIR` | No | Folder for the JSON and CSV files. Defaults to `output` |
   | `CSV_FILE` | No | Name of the summary CSV inside `OUTPUT_DIR`. Defaults to `summary.csv` |
   | `LOG_FILE` | No | File where errors are written. Defaults to `errors.log` |

   Keep `.env` private and never commit it, because it can contain your token.

## Usage

python main.py

Enter one or more usernames separated by commas, without spaces:

```
Enter GitHub usernames (Comma Separated Values): octocat,MehreenI
```

## Example output

The numbers below are from a real run. Yours will differ because profiles change over time.

**Terminal**

```
JSON saved: output\octocat.json
JSON saved: output\MehreenI.json
CSV saved: output\summary.csv
```

**`output/octocat.json`**: one file per user

```json
{
  "login": "octocat",
  "name": "The Octocat",
  "public_repos": 8,
  "followers": 24481
}
```

**`output/summary.csv`**: one row for each user that was fetched successfully

```csv
login,name,public_repos,followers
octocat,The Octocat,8,24481
MehreenI,Mehreen Imran,12,0
```

If no user is fetched successfully, the CSV is not created.

## Errors and retries

Errors are written to `errors.log`.
Failed requests are retried up to `MAX_RETRIES` times (default 3), waiting `RETRY_DELAY` seconds (default 2) between attempts.


## Project structure

```
github_profile_cl/
├── main.py            # the script
├── requirements.txt   # requests, python-dotenv
├── .example.env       # template for .env
├── .env               # your settings (private)
├── errors.log         # error log
└── output/            # JSON files and summary.csv
```
