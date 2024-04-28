import json
import os
import time


file_name = "auditoriums.json"

seat_sign = "O"
seat_booked = "X"
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def clear_screen():
    """Little function to clear the screen regardless of the OS."""

    os.system("cls" if os.name == "nt" else "clear")


def get_ids(data):
    """Get the ID of the last auditorium in the list (= the most recently added)
    in order to use it when creating a new auditorium by adding 1 to it."""

    if len(data) != 0:
        for auditorium in data:
            print(auditorium, auditorium["id"])
        return data[-1]["id"] + 1
    else:
        return 1


def menu_do_next(data):
    while True:
        available_choices = ["1", "2", "exit"]
        print("\nWhat would you like to do next?")
        print("1. Back to the list of auditoriums")
        print("2. Back to the main menu")
        print("exit. Exit the program")
        do_next = input("\tYour choice: ")
        if do_next not in available_choices:
            continue
        break

    if do_next == "1":
        display_auditoriums(data)
    elif do_next == "2":
        main()
    elif do_next == "exit":
        exit()


def auditorium_new_name(auditorium, data):
    """To name an auditorium upon creation OR update. The name must contain
    only letters from the alphabet, digits and spaces. Spaces before and after
    the name are automatically removed."""

    while True:
        type_again = False
        auditorium_name = input(
            "Auditorium name (spaces, alphabet letters and digits only - type 'back' to go back): "
        )
        auditorium_name = auditorium_name.strip()

        if auditorium_name == "back":
            break

        for char in auditorium_name:
            if char.isalnum() or char == " ":
                pass
            else:
                print(
                    f"\tERROR - Unauthorized character: {char}, please check and try again."
                )
                type_again = True
                break
        if type_again:
            continue

        while True:
            print(f"Name: {auditorium_name}")
            confirm_name = input("Is that name OK? (y/n) ").casefold()
            if confirm_name == "y" or confirm_name == "n":
                return confirm_name, auditorium_name, auditorium, data

    main()


def create_auditorium(data):
    """Create an auditorium. The ID is automatically added and the rows
    are empty by default."""

    clear_screen()
    print("| ADD AN AUDITORIUM |\n")
    auditorium = ""
    while True:
        confirm_name, auditorium_name, auditorium, data = auditorium_new_name(
            auditorium, data
        )
        if confirm_name == "y":
            new_auditorium = {
                "id": get_ids(data),
                "name": auditorium_name,
                "rows": [],
            }
            data.append(new_auditorium)
            with open(file_name, "w") as json_file:
                json.dump(
                    data,
                    json_file,
                    indent=4,
                )
            break
        continue
    main()


def delete_auditorium(auditorium, data):
    """Permanently delete the target auditorium after confirmation.
    The user can go also choose to go back to the menu."""

    while True:
        clear_screen()
        print(
            f"\t| DELETION MENU FOR [{auditorium['name']} (ID {auditorium['id']})] |\n"
        )

        print(
            f'You are about to permanently delete the auditorium "{auditorium["name"]}".'
        )
        confirm_delete = input(
            f'Are you sure? Type in "delete" to confirm or "back" to go back to the auditoriums list: '
        )
        if confirm_delete == "delete" or confirm_delete == "back":
            break

    if confirm_delete == "back":
        display_auditoriums(data)
    elif confirm_delete == "delete":
        print(f"DELETING {data[data.index(auditorium)]}")
        data.pop(data.index(auditorium))
        with open(file_name, "w") as json_file:
            json.dump(
                data,
                json_file,
                indent=4,
            )

    main()


def add_row(auditorium, data):
    """Add a row to an auditorium to a specific position with a given
    number of seats (>= 1). Leaving the position empty results in adding
    the row as the latest (after all the existing rows)."""

    if len(auditorium["rows"]) >= 1:
        while True:
            print(f'\nEnter the position of the row (1 to {len(auditorium["rows"])})')
            position_input = input("Leave it BLANK if you wish to add it at the end: ")
            if position_input == "":
                break
            try:
                u = int(position_input)
                position_input = int(position_input)
                if position_input not in range(1, len(auditorium["rows"]) + 1):
                    print("Number not valid.")
                    continue
                pass
            except ValueError:
                print("Bad input, only numbers are allowed.")
                continue
            break

    else:
        position_input = 0

    while True:
        try:
            print(
                "Note: each line in a row can contain up to 26 seats, with a maximum of 9 lines."
            )
            number_seats = int(input("How many seats to add? (max 234 seats): "))
        except ValueError:
            print("Please enter a valid number only.")
            continue
        if number_seats < 1:
            print("You need at least to add ONE seat.")
            continue
        if number_seats > 234:
            print("Too many seats, rows can contain up to 234 seats.")
            continue
        break
    row = []
    for s in range(number_seats):
        row.append(seat_sign)

    if number_seats == 1:
        seats_str = "seat"
    else:
        seats_str = "seats"
    print(f"This is the new row to add ({number_seats} {seats_str}):")
    print(row)
    while True:
        confirm_input = input("Please confirm (y/n): ").casefold()
        if confirm_input == "y" or confirm_input == "n":
            break
        continue

    if confirm_input == "y":
        if position_input == "":
            auditorium["rows"].append(row)
        else:
            auditorium["rows"].insert(position_input - 1, row)
        with open(file_name, "w") as json_file:
            json.dump(
                data,
                json_file,
                indent=4,
            )

        print("\nRow added successfully")
        menu_do_next(data)

    else:
        add_row(auditorium, data)


def no_row(auditorium, data):
    """Check if the auditorium has at least one row. If not, a menu
    is displayed to add a new row or get back to a menu."""

    choices = ["1", "2", "3", "exit"]

    if len(auditorium["rows"]) == 0:
        while True:
            print("That auditorium does not have rows yet.\n")
            print("1. Add a row")
            print("2. Back to the auditoriums list")
            print("3. Back to the main menu")
            print("exit. Exit the program")
            choice_input = input("\tYour choice: ")
            if choice_input in choices:
                break
        if choice_input == "1":
            add_row(auditorium, data)
        if choice_input == "2":
            display_auditoriums(data)
        if choice_input == "3":
            main()
        if choice_input == "exit":
            exit()

    else:
        pass


def delete_row(auditorium, data):
    """Delete a selected row."""

    display_auditorium_details(auditorium, data)

    no_row(auditorium, data)

    while True:
        try:
            row_choice = int(
                input(
                    f'Which row would you like to delete? 1-{len(auditorium["rows"])}: '
                )
            )
        except ValueError:
            print("Please enter a valid number only.")
            continue
        if row_choice not in range(1, len(auditorium["rows"]) + 1):
            print("That row does not exist.")
            continue

        while True:
            print(
                f'You wish to remove Row {row_choice}: {auditorium["rows"][row_choice-1]}'
            )
            del_confirm = input("Are you sure? (y/n)").casefold()
            if del_confirm == "y" or del_confirm == "n":
                break
            else:
                print("Wrong input.")
        if del_confirm == "y":
            break

    auditorium["rows"].pop(row_choice - 1)
    with open(file_name, "w") as json_file:
        json.dump(
            data,
            json_file,
            indent=4,
        )

    menu_do_next(data)


def seats_alpha_num(row):
    seat_letters = ""
    seats = ""
    seats_added = 0
    remaining = len(row)

    for s in range(len(row)):
        seat_number = (s // 26) + 1
        seat_letters += (
            f"{alphabet[s-(len(alphabet)*(s//len(alphabet)))]}{seat_number} | "
        )
        seats += f" {row[s]} | "
        seats_added += 1
        remaining -= 1
        if seats_added == 26 or remaining == 0:
            print(f"Seat number  - {seat_letters[:-2]}")
            print(f"Availability - {seats[:-2]}")
            seat_letters = ""
            seats = ""
            seats_added = 0
            print()


def display_seats(auditorium, row_choice):
    """Display the seats of a row with a letter for each seat
    to simplify the selection (to book/free/add/remove a seat)."""

    row = auditorium["rows"][row_choice - 1]

    seats_alpha_num(row)


def choose_seat(row, action_seat):
    if action_seat != "add":
        while True:
            seat_choice = input(f"Please choose a seat: ").upper()
            seat_index = alphabet.index(seat_choice[0]) + len(alphabet) * (
                int(seat_choice[1]) - 1
            )
            if seat_index > len(row) - 1:
                print("That seat does not exist")
                continue

            while True:
                confirm_seat = input(
                    f"You chose to {action_seat} seat {seat_choice} (y/n): "
                )
                if confirm_seat == "y" or confirm_seat == "n":
                    break
            if confirm_seat == "y":
                break

    else:
        while True:
            print("Please enter the position of the seat you wish to add.")
            print(
                "Leave the field BLANK if you wish to add the seat at the end of the row."
            )
            seat_choice = input(f"\tEnter an existing seat or leave blank): ").upper()
            if seat_choice != "":
                seat_index = int(
                    alphabet.index(seat_choice[0])
                    + len(alphabet) * (int(seat_choice[1]) - 1)
                )
                print(f"len {len(row)}, {seat_index}")
            if seat_choice == "" or 0 <= seat_index <= len(row) - 1:
                while True:
                    if seat_choice == "":
                        confirm_seat = input(
                            f"You chose to add a seat at the end of the row. (y/n) "
                        )
                    else:
                        confirm_seat = input(
                            f"You chose to add a seat at that position: {seat_choice}. (y/n) "
                        )
                    if confirm_seat == "y" or confirm_seat == "n":
                        break
                if confirm_seat == "y":
                    break

        if seat_choice == "":
            row.append(seat_sign)
        else:
            row.insert(seat_index, seat_sign)

    return seat_index


def book_unbook_seats(auditorium, data, choice):
    """A big function where a seat can be booked/unbooked/added/removed.
    Yes, it goes against the one function = one action rule, but it's more
    convenient that way as the process is more or less the same for each
    action."""

    display_auditorium_details(auditorium, data)

    while True:
        try:
            row_choice = int(
                input(f'Please choose the target row (1-{len(auditorium["rows"])}): ')
            )
        except ValueError:
            print("Please enter a valid number only.")
            continue
        if row_choice not in range(1, len(auditorium["rows"]) + 1):
            print("That row does not exist.")
            continue
        break

    while True:
        clear_screen()
        if choice == "4":
            print(
                f'\t| BOOK OR FREE A SEAT - Auditorium: {auditorium["name"]}, row {row_choice} |\n'
            )
        elif choice == "5":
            print(
                f'\t| ADD OR REMOVE A SEAT - Auditorium: {auditorium["name"]}, row {row_choice} |\n'
            )
        display_seats(auditorium, row_choice)

        if choice == "4":
            available_choices = ["1", "2", "back"]
            print("1. Book a seat")
            print("2. Free (unbook) a seat")
            print("back. Go back to the previous menu")
            action = input("\tYour choice: ")
            if action in available_choices:
                break

        elif choice == "5":
            available_choices = ["1", "2", "back"]
            print("1. Add a seat")
            print("2. Remove a seat")
            print("back. Go back to the previous menu")
            action = input("\tYour choice: ")
            if action in available_choices:
                break

    if action == "back":
        edit_auditorium(auditorium, data)

    if action == "1":
        if choice == "4":
            action_seat = "book"
        elif choice == "5":
            action_seat = "add"
    elif action == "2":
        if choice == "4":
            action_seat = "free"
        elif choice == "5":
            action_seat = "remove"

    row = auditorium["rows"][row_choice - 1]
    subrows = len(row) // len(alphabet) + 1
    print(f"subrows: {subrows}")

    seat_index = choose_seat(row, action_seat)

    if action_seat == "book":
        if row[seat_index] != seat_booked:
            row[seat_index] = seat_booked
            update = True
    elif action_seat == "free":
        if row[seat_index] != seat_sign:
            row[seat_index] = seat_sign
            update = True
    elif action_seat == "remove":
        del row[seat_index]
        update = True
    else:
        update = True

    if update:
        with open(file_name, "w") as json_file:
            json.dump(
                data,
                json_file,
                indent=4,
            )
        update = False

    print()
    if action_seat == "book":
        print("The seat was booked successfully.")
    elif action_seat == "free":
        print("The seat was unbooked successfully.")
    elif action_seat == "remove":
        print("The seat was removed successfully.")
    elif action_seat == "add":
        print("The seat was added successfully.")

    menu_do_next(data)


def display_auditoriums(data):
    clear_screen()
    print(f"\t| AVAILABLE AUDITORIUMS |\n")

    for t in range(len(data)):
        auditorium = data[t]
        print(f"{t+1}:", auditorium["name"])

    print("0. Back to the main menu")

    while True:
        try:
            selected_auditorium = int(input("\tSelect an auditorium: "))
        except ValueError:
            print("Please enter a valid number only.")
            continue
        if 0 <= selected_auditorium <= len(data):
            break
        else:
            print("That auditorium does not exist. Please try again.")
            continue

    if selected_auditorium == 0:
        main()

    else:
        auditorium = data[selected_auditorium - 1]
        display_auditorium_details(auditorium, data)
        edit_auditorium_menu(auditorium, data)


def display_auditorium_details(auditorium, data):
    clear_screen()
    print(f"\t| AUDITORIUM: {auditorium['name']} (ID {auditorium['id']}) |\n")

    no_row(auditorium, data)
    if len(auditorium["rows"]) == 0:
        print("That auditorium does not have rows yet.")

    else:
        print(
            f"{seat_sign}: available | {seat_booked}: booked | Seat number: A B C D..."
        )
        for r in range(len(auditorium["rows"])):
            row = auditorium["rows"][r]
            print(f"ROW {r+1}: {len(row)} seats")
            seats_alpha_num(row)
            print()


def edit_auditorium_menu(auditorium, data):
    choices = ["1", "2", "3", "4", "exit"]
    while True:
        clear_screen()
        print(
            f"\t| GENERAL MENU FOR [{auditorium['name']} (ID {auditorium['id']})] |\n"
        )

        display_auditorium_details(auditorium, data)

        print("1. Edit the auditorium")
        print("2. Delete the auditorium")
        print("3. Back to the list of auditoriums")
        print("4. Back to the main menu")
        print("exit. Exit the program")
        choice_input = input("\tYour choice: ")
        if choice_input in choices:
            break
    if choice_input == "1":
        edit_auditorium(auditorium, data)
    if choice_input == "2":
        delete_auditorium(auditorium, data)
    if choice_input == "3":
        display_auditoriums(data)
    if choice_input == "4":
        main()
    if choice_input == "exit":
        exit()


def edit_auditorium(auditorium, data):
    choices = ["1", "2", "3", "4", "5", "back", "exit"]
    while True:
        clear_screen()
        print(
            f"\t| EDITION MENU FOR [{auditorium['name']} (ID {auditorium['id']})] |\n"
        )

        display_auditorium_details(auditorium, data)

        print("1. Rename the auditorium")
        print("2. Add a row")
        print("3. Delete a row")
        print("4. Book/unbook a seat")
        print("5. Add/remove a seat")
        print("back. Back to the auditoriums list")
        print("exit. Exit the program")
        choice_input = input("\tYour choice: ")
        if choice_input in choices:
            break
    if choice_input == "1":
        rename_auditorium(auditorium, data)
    if choice_input == "2":
        add_row(auditorium, data)
    if choice_input == "3":
        delete_row(auditorium, data)
    if choice_input == "4":
        book_unbook_seats(auditorium, data, choice_input)
    if choice_input == "5":
        book_unbook_seats(auditorium, data, choice_input)
    if choice_input == "back":
        display_auditoriums(data)
    if choice_input == "exit":
        exit()


def rename_auditorium(auditorium, data):
    print(
        f"""Auditorium's current name: {auditorium["name"]} (ID {auditorium["id"]})"""
    )
    while True:
        confirm_name, auditorium_name, auditorium, data = auditorium_new_name(
            auditorium, data
        )
        if confirm_name == "y":
            auditorium["name"] = auditorium_name
            with open(file_name, "w") as json_file:
                json.dump(
                    data,
                    json_file,
                    indent=4,
                )
            break
        continue
    main()


def main_menu():
    """Main menu, when the program opens."""

    clear_screen()
    print("", "-" * 37)
    print("| AUDITORIUM MANAGER FOR THE POOR v1.0 |")
    print(f' {"-" * 37}')
    while True:
        choices = ["1", "2", "exit"]
        print("Please choose an option:")
        print("1. Add an auditorium")
        print("2. Display the auditoriums")
        print("exit. Exit the program")
        choice = input("\tYour choice: ")

        if choice in choices:
            return choice
        else:
            print("\n\tWrong input, please try again.\n")
            continue


def main():
    """Check if the file exists or not. If not, create it and redirect to
    auditorium creation. Also the case if the file is empty (only []).
    If the file exists, show the main menu."""

    empty_file = False
    while True:
        try:
            with open(file_name) as file:
                data = json.load(file)
                if len(data) == 0:
                    empty_file = True
                break
        except FileNotFoundError:
            with open(file_name, "w") as file:
                base = []
                json.dump(base, file)
                print(f'File "{file_name}" successfully created, loading...')
                time.sleep(1)
            continue

    if empty_file:
        empty_file = False
        create_auditorium(data)

    choice = main_menu()
    if choice == "1":
        create_auditorium(data)
    if choice == "2":
        display_auditoriums(data)
    if choice == "exit":
        exit()


if __name__ == "__main__":
    main()
