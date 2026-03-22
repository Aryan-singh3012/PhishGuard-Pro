import os
from supabase import create_client, Client

# These are your unique project credentials from the Supabase Dashboard
SUPABASE_URL = "https://gqoxufoyjhkyxxffclrl.supabase.co"
# REPLACE THE KEY BELOW with your actual 'anon' public key
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdxb3h1Zm95amhreXh4ZmZjbHJsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQxMTg4MzUsImV4cCI6MjA4OTY5NDgzNX0.jdC_b3UbAt-oNAa-WfxCsjIBE88txZTSjTor2JTBJBg"

# Initialize the Supabase Client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client initialized successfully.")
except Exception as e:
    print(f"Failed to initialize Supabase: {e}")

def log_scan_to_cloud(url: str, status: str, risk_score: float, reason: str):
    """
    Step 1: The Cloud Logger
    This function sends the analysis results from your Random Forest model 
    and SSL check directly to the Supabase 'scans' table.
    """
    try:
        # Prepare the data dictionary
        data = {
            "url": url,
            "status": status,
            "risk_score": float(risk_score),
            "reason": reason
        }
        
        # Insert the data into the 'scans' table
        response = supabase.table("scans").insert(data).execute()
        
        # Check if the insert was successful
        if response.data:
            print(f"Successfully logged to Cloud: {url}")
        else:
            print(f"Logging failed: No data returned from Supabase.")
            
    except Exception as e:
        print(f"Cloud Logging Error: {str(e)}")

# This allows you to test the file independently by running 'python3 backend/database.py'
if __name__ == "__main__":
    print("Testing Cloud Connection...")
    log_scan_to_cloud("http://test-site.com", "TEST", 50.0, "Initial connection test")