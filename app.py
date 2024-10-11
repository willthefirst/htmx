from flask import Flask, redirect, request, render_template

app = Flask(__name__)

class Contact:
    contacts = []

    def __init__(self, first_name, last_name, email, phone=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        Contact.contacts.append(self)  # Add the contact to the list upon creation

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone
        }

    @classmethod
    def all(cls):
        return cls.contacts

    @classmethod
    def search(cls, query):
        query = query.lower()
        return [contact for contact in cls.contacts if 
                query in contact.first_name.lower() or
                query in contact.last_name.lower() or
                query in contact.email.lower() or
                (contact.phone and query in contact.phone)]

# Instantiate some members of the Contact class
contact1 = Contact(first_name="John", last_name="Doe", email="john.doe@example.com", phone="123-456-7890")
contact2 = Contact(first_name="Jane", last_name="Smith", email="jane.smith@example.com")
contact3 = Contact(first_name="Alice", last_name="Johnson", email="alice.johnson@example.com", phone="098-765-4321")
                
@app.route("/")
def index():
    return redirect("/contacts")

@app.route("/contacts")
def contacts():
    search = request.args.get("q")
    if search is not None:
        print(search)
        contacts_set = Contact.search(search)
    else:
        contacts_set = Contact.all()    
    return render_template("index.html", contacts=contacts_set)

