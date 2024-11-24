import pandas as pd

# Function to segregate and save commands
def segregate_commands(input_file):
    # Read the CSV file
    data = pd.read_csv(input_file)

    # Segregate data based on command types
    set_data = data[data['Command'].str.startswith('set')]
    get_data = data[data['Command'].str.startswith('get')]
    delete_data = data[data['Command'].str.startswith('delete')]
    update_data = data[data['Command'].str.startswith('update')]

    # Save segregated data into separate files
    set_data.to_csv('set_commands.csv', index=False)
    get_data.to_csv('get_commands.csv', index=False)
    delete_data.to_csv('delete_commands.csv', index=False)
    update_data.to_csv('update_commands.csv', index=False)

    print("Files generated:")
    print("1. set_commands.csv")
    print("2. get_commands.csv")
    print("3. delete_commands.csv")
    print("4. update_commands.csv")

# Input file path
input_file = 'results_50_closed.csv'

# Call the function to segregate commands
segregate_commands(input_file)
