from classes import AddressBook
from handlers import add_contact, change_contact, contact_phone, all_contacts, add_birthday, show_birthday, birthdays
from handler_notebook import add_note, find_notes, modify_note, delete_note, find_note_by_id
from handler_notebook import notebook 
import re
blue = "\033[94m"
reset = "\033[0m"
green = '\033[92m'
red = '\033[91m'

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    
    try:
        notebook.load_from_file('notes.json')
    except FileNotFoundError:
        print("File not found. Starting with an empty notebook.")
    
    
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        
        elif command == "hello":
            print("How can I help you?")
            
        elif command == "add":
            response = add_contact(args, contacts)
            
            if 'overwrite' in response:
                option = input(response)
                try:
                    command = parse_input(option)[0]
                except ValueError:
                    print('Saving the contact was cancelled')
                    continue
                 
                if command == 'yes':
                    print(add_contact(args, contacts, True))
                else:
                    print('Saving the contact was cancelled')
            else:
                print(response)
                    
        elif command == 'change':
            print(change_contact(args, contacts))
            
        elif command == 'phone':
            print(contact_phone(args, contacts))
            
        elif command == 'all':
            print(all_contacts(contacts))
            
        elif command == 'add-birthday': 
            response = add_birthday(args, contacts)
            print(response)
            
        elif command == 'show-birthday':
            response = show_birthday(args, contacts)
            print(response)

        elif command == 'birthdays':
            birthdays(contacts)
     
# додавання окремої нотатки
        elif command == "nadd":
            # отримання тексту нотатки, дозволяються будь-які символи у будь-які послідовності. Якщо пусто, то скасовує операцію
            note_text = ' '.join(args) 
            if not note_text:
                print(f"{green}(^_^) No text entered. Note was not created.{reset}\n")
                continue 
        
            # отримання тегів, валідація тегів
            while True:
                tags_input = input(f"{blue}Enter tags separated by commas (optional): {reset}").strip()
                tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

                valid_tags = []
                invalid_tag_found = False
                
                for tag in tags:
                    if re.match(r'^\w+$', tag):
                        valid_tags.append(tag)
                    else:
                        print(f"{red}(>_<) Tag '{tag}' is invalid. Tags should contain only letters, numbers, and underscores.{reset}")
                        invalid_tag_found = True
                        break 
                # вихід з головного циклу, якщо всі теги дійсні
                if not invalid_tag_found:
                    break

            print(f"{green}(^_^) Note was successfully created.{reset}\n")
            add_note(note_text, valid_tags) 
            
# пошук нотатки за тегом та текстом (одночасно)            
        elif command == "nfind":
            search_args = ' '.join(args)
            tags = [arg for arg in search_args.split() if arg.startswith("#")]
            search_text = ' '.join(arg for arg in search_args.split() if not arg.startswith("#"))

            response = find_notes(tags=tags, search_text=search_text)        
               
    
# редагування нотатки
        elif command == "nedit":
            try:
                note_id = int(args[0]) if len(args) > 0 else int(input(f"{blue}Enter note ID: {reset}"))
            except:
                print(f"{red}(>_<) Invalid input.{reset}")
                continue   
            
            new_text = input(f"{blue}Enter new text for the note: {reset}")

            while True:
                tags_input = input(f"{blue}Enter tags separated by commas (optional): {reset}").strip()
                tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

                valid_tags = []
                invalid_tag_found = False
                
                for tag in tags:
                    if re.match(r'^\w+$', tag):
                        valid_tags.append(tag)
                    else:
                        print(f"{green}(>_<) Tag '{tag}' is invalid. Tags should contain only letters, numbers, and underscores. Separate multiple tags with commas.{reset}")
                        invalid_tag_found = True
                        break 
                
                if not invalid_tag_found:
                    break

            modify_note(note_id, new_text, valid_tags)

# видалення нотатки
        elif command == "ndel":
            delete_note(*args)
            
# показати нотатку
        elif command == "note":
            find_note_by_id(*args)           
            
        else:
            print(f"{red}Invalid command.{reset}")

if __name__ == "__main__":
    main()