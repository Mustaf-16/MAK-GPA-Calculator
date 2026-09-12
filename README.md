# MAK GPA Calculator

A polished Flask-based GPA calculator for MAK's 5.0 grading scale.

## Current status

This app is no longer just an initial Flask setup. It now includes:

- A responsive front-end GPA calculator interface
- Dynamic course entry rows with add/remove controls
- Support for entering either marks or letter grades
- Credit-weighted GPA calculation on the MAK 5.0 scale
- Academic classification output based on the final GPA
- JSON API endpoint for GPA calculation

## Features

- Add as many courses as needed
- Enter course name, credits, and either a mark or a grade
- Automatic conversion from marks to grades where applicable
- GPA returned to 2 decimal places
- Classification labels such as:
  - First Class
  - Second Class - Upper
  - Second Class - Lower
  - Pass
  - Below Pass

## Tech stack

- Python
- Flask
- Jinja2 templates
- Vanilla JavaScript
- CSS

## Project structure

- `app.py` — Flask entry point and web routes
- `routes/dashboard.py` — GPA calculation and classification logic
- `templates/` — HTML templates for the UI
- `static/js/` — client-side GPA form behavior
- `static/css/` — app styling

## Run locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the app:

   ```bash
   flask --app app run
   ```

3. Open the app in your browser at the local address shown by Flask.

## API endpoint

`POST /dashboard/gpa`

Example request body:

```json
{
  "courses": [
    { "credits": 3, "grade": "A" },
    { "credits": 2, "mark": 84 }
  ]
}
```

Example response:

```json
{
  "gpa": 4.5,
  "classification": "First Class"
}
```

## Notes

- The app uses the MAK 5.0 scale.
- Each course must include a positive credit value.
- A course can be evaluated using either a grade or a numeric mark.
