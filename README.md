# CLI Contact Book and Notes Application

## Project NeoNeo-7 - Team 16

## Team of Collaborators

Kostiantyn Skliar https://github.com/Arrakk-tur

Andrii Korchevnyi https://github.com/andreykorchevnyi

Mariia Savchuk https://github.com/MashaSavchuk

Ruslan Isupov https://github.com/Ruslan-Isupov

Roman Hubov https://github.com/NkPlast 


## Description

The CLI Contact Book and Notes App is a command-line tool designed to help you manage your contacts and take notes efficiently. It provides a simple and intuitive interface to add, view, update, and delete contact's information, as well as create and organize notes.


## Features

- Manage your contact list:
  - Add new contacts with name, phone number, email, address and birthday.
  - View a list of all your contacts.
  - Update existing contacts' information.
  - Delete contacts information from your list.
  - View list of contacts that have birthday for the next N days.

- System for handling notes:
  - Create and store your notes.
  - Display a list of all notes you have created.
  - Access and modify specific notes.
  - Erase notes that are no longer required.
  - Search for notes using both keywords and tags at the same time.
  - Attach and detach tags from specific notes.
  - Erase either the text or the tags within a note.
  

## Getting Started:

To use the Contact Book and Notes App, you'll need to follow steps below.

Installation:

1. **Be sure that you have Python installed on your machine either https://www.python.org/downloads/**

2. **Clone the Repository on your machine:**

   ```bash
   git clone https://github.com/Arrakk-tur/project-NeoNeo-7
   ```

Usage: Run main.py from application and follow the instructions and use bot commands.

The app provides a set of commands to interact with your contact list and notes.   


### Bot Commands

The following commands are supported by the bot:

hello: Welcoming command

add-contact [name] [phone]: Add a new contact with a name and phone number.
change-phone [name] [new phone]: Change the phone number for a specified contact.
show-phone [name]: Show phone of specific contact
show-contacts: Show all contacts

add-address [name] [address]: Add address
change-address [name] [old_address ] [new_address ]: Change address for specific contact
show-address [name]:Show address for specific contact
delete-address [name]  [address ]: Delete address for selected user

add-email "[name]" "[email]": Add email for selected user
change-email "[name]" "[old_email]" "[new_email]": Change email for specific contact
show-email "[name]":Show email for specific contact
delete-email "[name]" "[email]": Delete email for selected user

add-birthday "[name]" "[birth date]": Add a date of birth for a specified contact in format 01.01.1970
show-birthday "[name]": Show contact birthday
next_birthdays "[days]" (default=7 days): Show birthdays that will occur in the period of days passed as parameter. By default used 7 days.

naad first prompt: [text]:  Add text
    next prompt: [tags] separated by commas (optional): 	Add tags (optional)
nfind [keywords #tags]: Search by keywords and tags
nedit	[id]
	next prompt: [new-text] || [clear] (optional)		New text. Skip if nothing. Delete text if 'clear'
	next prompt: [new-tags] || [clear] (optional)		New tags. Skip if nothing. Delete text if 'clear' 			
ndel	[id]:	Delete note
note	[id]:	Show note with "id"

close or exit: Close the program.


### Examples
*   In terminal
    ```
    add-contact Masha 1234567890
    add-phone John 1234567890
    show-contacts

     ```


## Project Completion

This project aims to fulfill the following main requirements:

Efficient contact and note management
User-friendly experience with validation and reminders
Intuitive editing and deletion of records
For more details on project completion, please refer to the team of contributors.

Thank you for choosing the CLI Contact Book and Notes App. We hope it enhances your organization and productivity.
