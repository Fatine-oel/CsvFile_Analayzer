# CsvFile_Analyzer
This Django-based web application allows users to upload data files, perform statistical analysis, and visualize results interactively. Users can explore any row or column of data and view various statistical visualizations, providing an intuitive and engaging experience for data exploration and analysis
# CSV File Management with Statistical Analysis and Visualization

This Django project allows you to upload CSV files, perform statistical analysis on the data, and generate interactive visualizations.

## Features

- **CSV File Upload**: Users can upload a CSV file through a form.
- **Statistical Analysis**: Descriptive statistics are calculated for the selected columns, whether they are numerical or categorical.
- **Visualization**: The project generates various types of interactive charts to visualize the data (histogram, bar chart, scatter plot, etc.).

## Prerequisites

- Python 3.x
- Django
- Pandas
- Scikit-learn
- Plotly
- Matplotlib

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Fatine-oel/CsvFile_Analyzer.git
   cd CsvFile_Analyzer
Create a virtual environment and install the dependencies:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
pip install -r requirements.txt
Apply the database migrations:

bash
Copy code
python manage.py migrate
Start the development server:

bash
Copy code
python manage.py runserver
You can now access the app at http://127.0.0.1:8000/.

Usage
Upload a CSV File: Go to the homepage and upload a CSV file.
View Data: After uploading, you will be redirected to the page displaying the data.
Statistical Analysis: Select a column to obtain descriptive statistics like mean, median, standard deviation, etc.
Visualization: Select a chart type (histogram, bar chart, etc.) to visualize the data.
File Structure
gestion_fichiers/: Main folder containing the application code.
migrations/: Contains database migration files.
templates/: Contains HTML files for each page of the app.
home.html: Homepage with the upload form.
upload.html: Form to upload a CSV file.
view_data.html: Displays the data in a table format.
stat_analysis.html: Statistical analysis page with column selection.
visualisation.html: Visualization page with chart selection.
forms.py: Contains the form for uploading files.
views.py: Contains views for managing data display and analysis.
urls.py: Contains the app's URLs.
Contributing
Fork this repository.
Create a branch for your feature (git checkout -b feature/your-feature-name).
Commit your changes (git commit -am 'Add a new feature').
Push to your branch (git push origin feature/your-feature-name).
Open a Pull Request to merge your changes.
Authors
Fatine El Ouahdani
