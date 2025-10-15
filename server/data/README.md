# TigerTalks Data Population

This directory contains scripts to parse JSON data files and populate the TigerTalks database with course and semester information.

## Files

- `populate_models.py` - Main script to parse JSON data and populate database
- `run_data_population.py` - Simple runner script
- `data_utils.py` - Utility functions for data validation and cleanup
- `requirements.txt` - Additional Python dependencies
- `coursedetails.json` - Main course data with detailed information
- `pdf.json` - Course data with PDF requirements
- `departmentals.json` - Department and subject information

## Setup

1. Ensure you have the required dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure your `.env` file contains the MongoDB connection string:
   ```
   MONGODB_CONNECTION_STRING=your_mongodb_connection_string
   DATABASE_NAME=your_database_name
   ```

## Usage

### Populate Database

Run the main data population script:

```bash
# From the server directory
python run_data_population.py
```

Or run directly:

```bash
# From the server directory
python data/populate_models.py
```

### Data Validation and Cleanup

Run the data utilities:

```bash
python data/data_utils.py
```

## Data Structure

### Semester Model
- `_id`: MongoDB ObjectId
- `code`: Semester code (e.g., "1262")
- `name`: Semester name (e.g., "F25-26")
- `cal_name`: Calendar name (e.g., "Fall 2025")
- `reg_name`: Registration name (e.g., "25-26 Fall")
- `start_date`: Semester start date
- `end_date`: Semester end date

### Course Model
- `course_id`: Unique course identifier
- `catalog_number`: Course catalog number
- `title`: Course title
- `semester`: Semester code
- `department`: Department code
- `description`: Course description
- `pdf`: PDF requirements
- `grading`: Grading components and weights
- `instructors`: List of instructors
- `crosslistings`: Cross-listed courses
- `classes`: Class sections with schedules

## Data Sources

1. **coursedetails.json**: Primary source with comprehensive course information including:
   - Course details and descriptions
   - Instructor information
   - Class schedules and meeting times
   - Cross-listings
   - Building and room information

2. **pdf.json**: Secondary source with:
   - PDF requirements
   - Grading information
   - Basic course metadata

3. **departmentals.json**: Department information:
   - Department codes and names
   - Subject listings

## Features

- **Duplicate Prevention**: Scripts check for existing data before insertion
- **Data Validation**: Comprehensive validation of required fields
- **Error Handling**: Robust error handling with detailed logging
- **Data Merging**: Intelligent merging of data from multiple sources
- **Database Statistics**: Tools to check database status and find duplicates

## Logging

The scripts use Python's logging module with the following levels:
- INFO: General progress information
- WARNING: Non-critical issues
- ERROR: Critical errors that prevent processing
- DEBUG: Detailed debugging information

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**: Check your connection string in `.env`
2. **Missing JSON Files**: Ensure all JSON files are in the `data/` directory
3. **Memory Issues**: For large datasets, consider processing in batches
4. **Duplicate Data**: Use `data_utils.py` to find and remove duplicates

### Database Cleanup

To clear all data and start fresh:

```python
from data.data_utils import DataValidator
validator = DataValidator()
validator.clear_collections()
validator.close()
```

## Performance Notes

- The script processes data in batches to manage memory usage
- Duplicate checking is performed to avoid redundant insertions
- Database connections are properly managed and closed
- Large JSON files are processed efficiently using streaming techniques where possible
