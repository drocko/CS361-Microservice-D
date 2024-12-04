import zmq
import json


def client_main():
    context = zmq.Context()
    print(">>> Client attempting to connect to server...")
    socket = context.socket(zmq.REQ)
    server_ip = "localhost"  # Replace with actual server IP if not local
    socket.connect(f"tcp://{server_ip}:5555")

    while True:
        print("\nChoose an action to perform:")
        print("1. Create Entry")
        print("2. Read Entries")
        print("3. Update Entry")
        print("4. Delete Entry")
        print("5. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":  # Create
            date = input("Enter the date (YYYY-MM-DD): ").strip()
            amount = input("Enter water amount: ").strip()
            unit = input("Enter unit (e.g., oz, liters, cups): ").strip()
            request = {
                "action": "create",
                "data": {"date": date, "amount": amount, "unit": unit}
            }
        elif choice == "2":  # Read
            request = {"action": "read", "data": {}}
        elif choice == "3":  # Update
            date = input("Enter the date of the entry to update (YYYY-MM-DD): ").strip()
            amount = input("Enter new water amount: ").strip()
            unit = input("Enter new unit (e.g., oz, liters, cups): ").strip()
            request = {
                "action": "update",
                "data": {"date": date, "amount": amount, "unit": unit}
            }
        elif choice == "4":  # Delete
            date = input("Enter the date of the entry to delete (YYYY-MM-DD): ").strip()
            request = {
                "action": "delete",
                "data": {"date": date}
            }
        elif choice == "5":  # Quit
            print("Exiting client...")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        try:
            print(f">>> Sending request to server: {request}")
            socket.send_json(request)
            response = socket.recv_json()
            print(f">>> Server response: {json.dumps(response, indent=2)}")
        except Exception as e:
            print(f"Error communicating with the server: {e}")

    context.destroy()


if __name__ == "__main__":
    client_main()