from flask import Flask, request, render_template_string
import re


def modify_lines(text):
    # Define the pattern to search for lines with "from" or "join" followed by any number of whitespaces and two words separated by "."
    pattern = re.compile(r"\b(from|join)\s+(\w+)\.(\w+)", re.IGNORECASE)

    # Split the text into lines
    lines = text.split("\n")

    # Iterate over each line and modify if it matches the pattern
    modified_lines = []
    for line in lines:
        match = pattern.search(line)
        if match:
            modified_line = line.replace(match.group(2), f"$${{DB}}.{match.group(2)}")
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    # Join the modified lines back into a single string
    modified_text = "\n".join(modified_lines)

    return modified_text


def replace_sql_keywords(text):
    # Define the keywords and their replacements
    replacements = {
        r"\bselect\b": "SELECT",
        r"\bcase\b": "CASE",
        r"\bwhen\b": "WHEN",
        r"\bthen\b": "THEN",
        r"\belse\b": "ELSE",
        r"\bdeclare\b": "DECLARE",
        r"\bbegin\b": "BEGIN",
        r"\bend\b": "END",
        r"\bend as\b": "END AS",
        r"\bcoalesce\b": "COALESCE",
        r"\bas\b": "AS",
        r"\bupper\b": "UPPER",
        r"\blower\b": "LOWER",
        r"\bwhere\b": "WHERE",
        r"\bnot like\b": "NOT LIKE",
        r"\blike\b": "LIKE",
        r"\brlike\b": "RLIKE",
        r"\binitcap\b": "INITCAP",
        r"\bsubstring\b": "SUBSTRING",
        r"\blen\b": "LEN",
        r"\breplace\b": "REPLACE",
        r"\bqualify\b": "QUALIFY",
        r"\band\b": "AND",
        r"\bor\b": "OR",
        r"\bleft\b": "LEFT",
        r"\bright\b": "RIGHT",
        r"\binner\b": "INNER",
        r"\bfull\b": "FULL",
        r"\bjoin\b": "JOIN",
        r"\bunion\b": "UNION",
        r"\bunion all\b": "UNION ALL",
        r"\bminus\b": "MINUS",
        r"\bon\b": "ON",
        r"\bupdate\b": "UPDATE",
        r"\bset\b": "SET",
        r"\bdrop table\b": "DROP TABLE",
        r"\bcreate table\b": "CREATE TABLE",
        r"\bcreate or replace table\b": "CREATE OR REPLACE TABLE",
        r"\bcreate temporary table\b": "CREATE TEMPORARY TABLE",
        r"\bcreate or replace temporary table\b": "CREATE OR REPLACE TEMPORARY TABLE",
        r"\bcreate or replace procedure\b": "CREATE OR REPLACE PROCEDURE",
        r"\binsert into\b": "INSERT INTO",
        r"\binsert overwrite into\b": "INSERT OVERWRITE INTO",
        r"\btruncate table\b": "TRUNCATE TABLE",
        r"\bdelete from\b": "DELETE FROM",
        r"\bif exists\b": "IF EXISTS",
        r"\bif not exists\b": "IF NOT EXISTS",
        r"\bis null\b": "IS NULL",
        r"\bis not null\b": "IS NOT NULL",
        r"\b::date\b": "::DATE",
        r"\b::timestamp\b": "::TIMESTAMP",
        r"\b::timestamp_ntz\b": "::TIMESTAMP_NTZ",
    }

    # Replace each keyword in the text
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text


app = Flask(__name__)


# antdesign
# <link href="https://cdnjs.cloudflare.com/ajax/libs/antd/4.16.13/antd.min.css" rel="stylesheet">
@app.route("/", methods=["GET"])
def index():

    return render_template_string(
        """
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>SQL Keyword Replacer</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <style>
                .container {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    margin-top: 50px;
                }
                .box {
                    width: 40%;
                }
                textarea {
                    width: 100%;
                    height: 400px;
                }
            </style>
            <script>
                let timeout = null;
                function delayedSubmit(form) {
                    clearTimeout(timeout);
                    timeout = setTimeout(() => {
                        form.submit();
                    }, 1000);
                }
            </script>
          </head>
          <body>
            <div class="container">
              <div class="box">
                <h2>Input Text</h2>
                <form action="/submit" method="post">
                  <textarea class="form-control" id="input_text" name="input_text" rows="20" oninput="delayedSubmit(this.form)"></textarea>
              </div>
              </form>
              <div class="box">
                <h2>Modified Text</h2>
                <textarea class="form-control" id="modified_text" rows="20" readonly></textarea>
              </div>
            </div>
          </body>
        </html>
    """
    )


@app.route("/submit", methods=["POST"])
def submit():
    print("Hello")
    input_text = request.form.get("input_text", "")
    modified_text = replace_sql_keywords(modify_lines(input_text)) if input_text else ""
    print("Hello2")

    return render_template_string(
        """
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>SQL Keyword Replacer</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <style>
                .container {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    margin-top: 50px;
                }
                .box {
                    width: 40%;
                }
                .button-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    width: 20%;
                }
                textarea {
                    width: 100%;
                    height: 400px;
                }
            </style>
            <script>
                let timeout = null;
                function delayedSubmit(form) {
                    clearTimeout(timeout);
                    timeout = setTimeout(() => {
                        form.submit();
                    }, 1000);
                }
                
                function copyToClipboard() {
                    var copyText = document.getElementById("modified_text");
                    copyText.select();
                    copyText.setSelectionRange(0, 99999); // For mobile devices
                    document.execCommand("copy");
                }
            </script>
          </head>
          <body>
            <div class="container">
              <div class="box">
                <h2>Input Text</h2>
                <form method="post">
                  <textarea class="form-control" id="input_text" name="input_text" rows="20" oninput="delayedSubmit(this.form)">{{ input_text }}</textarea>
              </div>
              </form>
              <div class="button-container mt-3">
                <form action="/" method="get">
                  <button type="submit" class="btn btn-secondary">Clear</button>
                </form>
              </div>
              <div class="box">
                <h2>Modified Text</h2>
                <textarea class="form-control" id="modified_text" rows="20" readonly>{{ modified_text }}</textarea>
                <button class="ant-btn ant-btn-primary mt-3" onclick="copyToClipboard()">Copy</button>
              </div>
            </div>
          </body>
        </html>
    """,
        input_text=input_text,
        modified_text=modified_text,
    )


if __name__ == "__main__":
    app.run(debug=True)
