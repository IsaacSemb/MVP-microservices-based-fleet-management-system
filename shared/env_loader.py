import os
from dotenv import load_dotenv

def load_env():
    """
    Load the appropriate environment file based on the `FLASK_ENV_FILE` environment variable.
    Defaults to `.env.local` if `FLASK_ENV_FILE` is not set.
    """
    # Determine the environment file to load
    env_file = os.getenv('FLASK_ENV_FILE', '.env.local')

    # Load the .env file
    if os.path.exists(env_file):
        print(env_file)
        load_dotenv(env_file)
        print(f"Loaded environment variables from {env_file}")
    else:
        raise FileNotFoundError(f"The specified env file '{env_file}' does not exist.")

# Call this function on import if you want auto-loading, otherwise explicitly call it in your code.
if __name__ == "__main__":
    load_env()
    print(os.getenv('DRIVER_SERVICE_URL'))
    
