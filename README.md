# Google Sheets-Based Academic Webpage

This is something I built for myself but I could imagine others finding it useful. 

## Make a Google Sheets file with the appropriate sheets and columns
Here is [mine](https://docs.google.com/spreadsheets/d/1EqL3ArudCVWcmJZd2NgC8rK_diIk7dyH4Ws2TRKRBnU/). 

## Modify the `.env` file 
```
GOOGLE_SHEETS_URL="https://docs.google.com/spreadsheets/d/1EqL3ArudCVWcmJZd2NgC8rK_diIk7dyH4Ws2TRKRBnU/export?format=xlsx"
```

## Put your photo in the `images` folder and call in `me.jpeg`

# Software Help Guide

This guide provides instructions on how to use the software for pulling data from a structured spreadsheet and creating an academic webpage. The process is managed through a `Makefile` which contains various commands to automate the tasks.

## Makefile Commands

### .PHONY: refresh
- **Purpose**: This is a pseudo-target that helps in refreshing the data.
- **Usage**: Run `make refresh` in the terminal.
- **Action**: Executes the `pull_data.py` script using Python 3 to refresh or pull new data.

### refresh:
- **Python Version**: Python 3
- **Script**: `pull_data.py`
- **Description**: This command pulls the latest data from the source and updates the local dataset.

### data/my_database.db: pull_data.py
- **Purpose**: To ensure that the database is updated whenever `pull_data.py` changes.
- **Usage**: Automatically triggered when `pull_data.py` is modified.
- **Action**: Runs `pull_data.py` to update `my_database.db` with the latest data.

### website.md: templates/website.md create_website.py data/my_database.db
- **Dependencies**: 
  - Template file: `templates/website.md`
  - Script: `create_website.py`
  - Database: `data/my_database.db`
- **Purpose**: To generate the markdown file `website.md` for the website.
- **Usage**: Run `make website.md` to generate the markdown file.
- **Action**: Executes `create_website.py` script using Python 3.9, which uses the data from `my_database.db` to create `website.md` based on the template.

### index.html: website.md style.css
- **Dependencies**: 
  - Markdown file: `website.md`
  - CSS file: `style.css`
- **Purpose**: To convert `website.md` to `index.html` and apply styles.
- **Usage**: Run `make index.html` after updating `website.md` or `style.css`.
- **Action**: Uses `pandoc` to convert `website.md` into an HTML file (`index.html`) and applies the CSS styles from `style.css`. The page title is set to "John Horton's Academic Website".

### website: index.html
- **Purpose**: To view the generated website locally.
- **Usage**: Run `make website`.
- **Action**: Opens `index.html` in Firefox for previewing the website.

### update:
- **Purpose**: To update the Git repository with the latest changes.
- **Usage**: Run `make update` after making changes to the project files.
- **Action**: Adds all updated files to Git, commits them with a message "Updates", and pushes the changes to the `master` branch on the remote origin.

## Additional Notes
- **Python Version**: Ensure that the correct version of Python (as specified in the commands) is installed and accessible from your terminal.
- **Git**: The `update` command assumes that the project is a Git repository and the remote named `origin` is set up.
- **Pandoc**: Ensure that Pandoc is installed for the conversion of markdown to HTML.
