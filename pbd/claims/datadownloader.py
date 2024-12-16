import psycopg2
import pandas as pd

# Database connection parameters
db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '1234',
    'host': 'local',
    'port': '5432'  # Default is 5432 for PostgreSQL
}

# SQL query to fetch data
query = """
SELECT  
    primary_key, 
    unique_primary_key, 
    source_system, 
    claim_number, 
    policy_number, 
    general_nature_of_loss, 
    cause_of_loss, 
    line_of_business, 
    claim_received_date, 
    claim_loss_date, 
    claim_finalised_date, 
    loss_location_address_line_1, 
    loss_location_address_line_2, 
    loss_location_address_line_3, 
    loss_location_city, 
    loss_location_post_code, 
    loss_location_state, 
    loss_location_country, 
    claim_description, 
    original_verified_date_of_loss_time, 
    last_verified_date_of_loss_time, 
    claim_status, 
    claim_decision_status, 
    authorised_to_lodge_flag, 
    next_contact_reason, 
    reason_for_delay, 
    claim_owner_first_name, 
    claim_owner_last_name, 
    how_claim_reported_type, 
    fault_rating, 
    fault_categorisation, 
    contact_frequency, 
    excess_waived_flag, 
    excess_edit_reason, 
    excess_modified_reason, 
    excess_waived_reason, 
    indemnity_status, 
    total_open_recovery_reserve, 
    total_open_remaining_reserve, 
    total_open_future_payment, 
    total_recovery, 
    total_net_incurred, 
    total_paid, 
    property_total_loss_indicator, 
    notify_only_claim_flag, 
    type_of_worker, 
    claim_involve_injured_worker_flag, 
    catastrophe_code, 
    catastrophe_name, 
    vehicle_total_loss_indicator, 
    catastrophe_valid_from_date_time, 
    catastrophe_valid_to_date_time, 
    update_date
FROM public.claim_details limit 200000;
"""

# Filepath to save the CSV file
output_csv_path = "claim_details.csv"

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**db_params)

    # Read the data into a pandas DataFrame
    df = pd.read_sql_query(query, connection)

    # Save the DataFrame to a CSV file
    df.to_csv(output_csv_path, index=False)
    print(f"Data has been exported to {output_csv_path}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure the connection is closed
    if 'connection' in locals() and connection:
        connection.close()
