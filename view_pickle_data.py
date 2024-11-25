import pickle

# file paths
PRODUCTS_FILE = 'products_data.pkl'
USERS_FILE = 'user_data.pkl'

def load_data(file_path):
    """Load data from a pickle file."""
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return f"The file {file_path} does not exist."
    except Exception as e:
        return f"An error occurred while loading {file_path}: {e}"

def view_data():
    """Display data from the pickle files."""
    print("Choose the data you want to view:")
    print("1. Products Data")
    print("2. Users Data")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        data = load_data(PRODUCTS_FILE)
        print("\n--- Products Data ---")
        print(data if isinstance(data, dict) else data)
    elif choice == '2':
        data = load_data(USERS_FILE)
        print("\n--- Users Data ---")
        print(data if isinstance(data, dict) else data)
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    view_data()
