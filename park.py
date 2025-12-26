import os
from datetime import datetime

BOOKING_FILE = 'bookings.txt'
TOTAL_SLOTS = 10

def load_bookings():
    bookings = {}
    if os.path.exists(BOOKING_FILE):
        with open(BOOKING_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 4:
                    slot, username, vehicle, timestamp = parts
                    bookings[int(slot)] = (username, vehicle, timestamp)
    return bookings

def save_bookings(bookings):
    with open(BOOKING_FILE, 'w') as f:
        for slot, (username, vehicle, timestamp) in bookings.items():
            f.write(f"{slot},{username},{vehicle},{timestamp}\n")

def signup(users):
    username = input("Enter new username: ")
    if username in users:
        print("Username already exists.\n")
        return None
    password = input("Enter password: ")
    users[username] = password
    print("Signup successful!\n")
    return username

def login(users):
    username = input("Enter username: ")
    password = input("Enter password: ")
    if users.get(username) == password:
        print(f"Welcome, {username}!\n")
        return username
    else:
        print("Invalid credentials.\n")
        return None

def show_slots(bookings):
    print("\n--- Parking Slots ---")
    for slot in range(1, TOTAL_SLOTS + 1):
        if slot in bookings:
            user, vehicle, time = bookings[slot]
            print(f"Slot {slot}: Booked by {user} | Vehicle: {vehicle} | At: {time}")
        else:
            print(f"Slot {slot}: Available")
    print()

def book_slot(bookings, username):
    show_slots(bookings)
    try:
        slot = int(input(f"Choose a slot (1-{TOTAL_SLOTS}): "))
        if slot < 1 or slot > TOTAL_SLOTS:
            print("Invalid slot number.")
            return
        if slot in bookings:
            print("Slot already booked.")
            return
        vehicle = input("Enter your vehicle number: ")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        bookings[slot] = (username, vehicle, timestamp)
        save_bookings(bookings)
        print(f"Slot {slot} booked successfully!\n")
    except ValueError:
        print("Invalid input.\n")

def cancel_booking(bookings, username):
    found = False
    for slot, (user, _, _) in list(bookings.items()):
        if user == username:
            del bookings[slot]
            save_bookings(bookings)
            print(f"Booking for slot {slot} cancelled.\n")
            found = True
            break
    if not found:
        print("No booking found.\n")

def update_booking(bookings, username):
    current_slot = None
    for slot, (user, _, _) in bookings.items():
        if user == username:
            current_slot = slot
            break

    if current_slot is None:
        print("No booking found to update.\n")
        return

    print(f"\nYour current booking: Slot {current_slot}")
    try:
        new_slot = int(input(f"Enter new slot number (1-{TOTAL_SLOTS}): "))
        if new_slot < 1 or new_slot > TOTAL_SLOTS:
            print("Invalid slot number.")
            return
        if new_slot != current_slot and new_slot in bookings:
            print("Slot already booked by someone else.")
            return

        new_vehicle = input("Enter new vehicle number: ")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        del bookings[current_slot]
        bookings[new_slot] = (username, new_vehicle, timestamp)
        save_bookings(bookings)
        print(f"Updated to Slot {new_slot} with vehicle {new_vehicle}.\n")
    except ValueError:
        print("Please enter a valid number.\n")

def main():
    users = {"admin": "admin123"}  # Predefined user
    bookings = load_bookings()

    while True:
        print("--- Parking Booking System ---")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            user = login(users)
            if user:
                while True:
                    print("\n--- Main Menu ---")
                    print("1. View Slots")
                    print("2. Book Slot")
                    print("3. Cancel My Booking")
                    print("4. Update My Booking")
                    print("5. Logout")
                    option = input("Enter your choice: ")

                    if option == '1':
                        show_slots(bookings)
                    elif option == '2':
                        book_slot(bookings, user)
                    elif option == '3':
                        cancel_booking(bookings, user)
                    elif option == '4':
                        update_booking(bookings, user)
                    elif option == '5':
                        print("Logged out.\n")
                        break
                    else:
                        print("Invalid choice.\n")

        elif choice == '2':
            signup(users)

        elif choice == '3':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()
