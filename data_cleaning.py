import pandas as pd

# Load the tab-delimited datasets with appropriate encoding
section_data = pd.read_csv('data/section', delimiter='\t', encoding='latin1')
term_data = pd.read_csv('data/term', delimiter='\t', encoding='latin1')
student_cap_data = pd.read_csv('data/student_cap', delimiter='\t', encoding='latin1')
instruction_data = pd.read_csv('data/instruction', delimiter='\t', encoding='latin1')
delivery_data = pd.read_csv('data/delivery', delimiter='\t', encoding='latin1')

# Corrected path for course data
course_data_path = "data/course"
course_data = pd.read_csv(course_data_path, delimiter='\t', encoding='latin1')

# Ensure the 'description' column exists in the course_data
if 'description' not in course_data.columns:
    raise ValueError("The 'description' column is missing from the course data.")

# Remove duplicate courses based on 'course_code'
course_data = course_data.drop_duplicates(subset=['course_code'])

# Merge datasets based on common columns
# Merge section_data with term_data on 'term_code'
merged_data = pd.merge(section_data, term_data, on='term_code', how='left')

# Merge with student_cap_data on 'section_id'
merged_data = pd.merge(merged_data, student_cap_data, on='section_id', how='left')

# Merge with instruction_data on 'section_id'
merged_data = pd.merge(merged_data, instruction_data, on='section_id', how='left')

# Merge with delivery_data on 'delivery_code'
merged_data = pd.merge(merged_data, delivery_data, on='delivery_code', how='left')

# Merge with course_data on 'course_code'
final_data = pd.merge(merged_data, course_data, on='course_code', how='left')

# Select relevant columns, including the description
final_columns = [
    'course_code', 'title', 'dept_code',
    'credits', 'pre_reqs', 'core_area', 'inquiry_area', 'recommendation', 'description'
]

# Ensure the selected columns exist in the final data
final_columns = [col for col in final_columns if col in final_data.columns]
final_data = final_data[final_columns]

# Fill missing values with False
final_data.fillna(False, inplace=True)

# Remove duplicate courses based on all columns in the final data
final_data = final_data.drop_duplicates()

# Save the cleaned and merged data to a new CSV file
final_data.to_csv('data/cleaned_merged_data2.csv', index=False)

# Display the first few rows of the cleaned and merged data
print(final_data.head())
