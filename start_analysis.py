import subprocess
import sys

def main():
    print("=====================================================")
    print("   Starting SQL Relational Analysis Environment...   ")
    print("=====================================================")
    print("Launching Streamlit dashboard...\n")
    try:
        # Use subprocess to run the streamlit command
        subprocess.run(["streamlit", "run", "src/main.py"], check=True)
    except FileNotFoundError:
        print("Error: 'streamlit' command not found.")
        print("Please ensure you have activated your virtual environment")
        print("and installed the requirements (pip install -r requirements.txt).")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nDashboard shut down gracefully.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
