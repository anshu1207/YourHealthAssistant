1. START

2. Initialize the SQLite database
   └── Create a 'patient' table with fields: ID, Name, Age, Symptom

3. Start the Flask API server
   ├── Endpoint /add      → Receives JSON data and inserts it into the database
   └── Endpoint /patients → Returns all saved patient data in JSON format

4. Launch the Tkinter GUI
   ├── Input Fields: Name, Age, Symptom
   ├── Button: Submit
       └── Sends data to Flask API (/add) via POST request
   └── Button: Visualize
       └── Reads data from the database using Pandas
       └── Plots bar chart of symptom frequency using Matplotlib

5. Save the visualization as an image (symptoms_chart.png)

6. Display success message and reset the form

7. END

For more information


🔁 Step-by-Step Algorithm
Start the Application

The application begins execution with the initialization of necessary libraries (Flask, Tkinter, SQLite, Pandas, etc.).

Initialize SQLite Database

A database file named health.db is created (if it doesn’t exist).

A table patient is defined with columns: id, name, age, and symptom.

Start Flask Backend API

The Flask server runs locally and exposes two main endpoints:

POST /add: Accepts patient data in JSON format and inserts it into the SQLite database.

GET /patients: Returns a list of all saved patients in JSON format for further use.

Launch Tkinter GUI

A graphical form is displayed using Tkinter with input fields for:

Patient Name

Age

Symptom Description

The GUI includes two buttons:

Submit:

Sends the filled data to the Flask API (/add) using the requests module.

Shows a popup message on successful submission.

Visualize:

Fetches all records from the SQLite database using Pandas.

Uses Matplotlib to generate a bar chart showing frequency of each symptom.

Saves the plot as symptoms_chart.png.

Save and Display Output

The entered patient data is stored in health.db.

A bar chart is generated and saved, giving visual insights into common health symptoms.

Reset the Form

After data submission, the form fields are cleared for the next input.

End

The application continues to run until manually exited by the user.
