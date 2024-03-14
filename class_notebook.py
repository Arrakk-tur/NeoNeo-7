from datetime import datetime
import json
blue = '\033[94m'
reset = '\033[0m'
green = '\033[92m'
red = '\033[91m'

class Note:
    _last_id = 0
    
    def __init__(self, text, tags=None):
        Note._last_id += 1
        self.id = Note._last_id
        self.text = text
        self.tags = set(tags) if tags else set()
        self.creation_date = datetime.today()

    def modify(self, new_text):
        self.text = new_text

    def set_tags(self, tags):
        for tag in tags:
            self.tags = set(tags)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'tags': list(self.tags),
            'creation_date': self.creation_date.strftime('%Y-%m-%d %H:%M:%S')
        }

    @staticmethod
    def from_dict(data):
        note = Note(data['text'], data['tags'])
        note.id = data['id']
        note.creation_date = datetime.strptime(data['creation_date'], '%Y-%m-%d %H:%M:%S')
        return note

    
    def __repr__(self):
        return f'Note(id={self.id}, text="{self.text}", tags={self.tags}, creation_date={self.creation_date})'

class Notebook:
    def __init__(self):
        self.notes = []

    def add_note(self, text, tags=None):
        self.notes.append(Note(text, tags))
        self.save_to_file('notes.json')

    def find_notes(self, tags=None, text=None):
        found_notes = self.notes

        if tags:
            found_notes = [note for note in found_notes if any(tag in note.tags for tag in tags)]

        if text:
            found_notes = [note for note in found_notes if text in note.text]

        return found_notes
    
    def _find_note_by_id(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None
        

    def modify_note(self, note_id, new_text):
        for note in self.notes:
            if note.id == note_id:
                if new_text == 'clear':
                    new_text = ''
                    
                note.modify(new_text)
                print(f"Text of the Note with ID {note_id} has been modified.")
                self.save_to_file('notes.json')
                break
            
        
    def modify_tags(self, note_id, new_tags):
        for note in self.notes:
            if note.id == note_id:
                if new_tags == ['clear']: 
                    note.set_tags(set())
                    print(f"{green}All tags of the Note with ID {note_id} have been cleared.\n{reset}")
                else:
                    note.set_tags(new_tags)
                    print(f"Tags of the Note with ID {note_id} has been modified.\n")
                    
        self.save_to_file('notes.json')
            

    def delete_note(self, note_id):
        note_to_delete = None
        for note in self.notes:
            if note.id == note_id:
                note_to_delete = note
                break

        if note_to_delete:
            self.notes.remove(note_to_delete)
            print(f"Note with ID {note_id} has been deleted.")
            self.save_to_file('notes.json')
        else:
            print(f"No note found with ID {note_id}.")
    
    def find_note_by_id(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None
    
    
    def save_to_file(self, file_name):
        with open(file_name, 'w') as file:
            notes_dict = [note.to_dict() for note in self.notes]
            json.dump(notes_dict, file, indent=4)
    
    def load_from_file(self, file_name):
        with open(file_name, 'r') as file:
            notes_dict = json.load(file)
            self.notes = [Note.from_dict(note_data) for note_data in notes_dict]
