from flask import Flask, redirect, request, render_template, flash

app = Flask(__name__)
app.secret_key = 'wills_secret_key'

class Contact:
    contacts = []
    next_id = 1

    def __init__(self, first_name=None, last_name=None, phone=None, email=None):
        self.id = str(Contact.next_id)
        Contact.next_id += 1

        self.first = first_name
        self.last = last_name
        self.email = email
        self.phone = phone
        self.errors = {
            email: None
        }
    def __str__(self):
        return f"{self.first} {self.last} ({self.email})"

    def to_dict(self):
        return {
            'first': self.first,
            'last_name': self.last,
            'email': self.email,
            'phone': self.phone
        }
    
    def save(self):
        existing_contact = Contact.find(self.id)
        if existing_contact:
            # Update existing contact
            for attr in ['first', 'last', 'email', 'phone']:
                setattr(existing_contact, attr, getattr(self, attr))
            return True
        else:
            # Insert new contact
            Contact.contacts.append(self)
            return True
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return True
    
    def validate(self):
        if self.email == "error@example.com":
            self.errors["email"] = "Bad email"
        else:
            self.errors.clear()

    @classmethod
    def all(cls, page=1, per_page=10):
        start = (page - 1) * per_page
        end = start + per_page
        return cls.contacts[start:end]

    @classmethod
    def search(cls, query):
        query = query.lower()
        return [contact for contact in cls.contacts if 
                query in contact.first.lower() or
                query in contact.last.lower() or
                query in contact.email.lower() or
                (contact.phone and query in contact.phone)]
    
    @classmethod
    def find(cls, id):
        return next((contact for contact in cls.contacts if contact.id == id), None)
    
    @classmethod
    def delete(cls, id):
        contact = cls.find(id)
        if contact:
            cls.contacts.remove(contact)
            return True
        return False
    
    @classmethod
    def count(cls):
        return len(cls.contacts)
    
# List of contact information
contacts_data = [
    {"first_name": "John", "last_name": "Doe", "phone": "123-456-7890", "email": "john.doe@example.com"},
    {"first_name": "Jane", "last_name": "Smith", "email": "jane.smith@example.com"},
    {"first_name": "Alice", "last_name": "Johnson", "phone": "098-765-4321", "email": "alice.johnson@example.com"},
    {"first_name": "Bob", "last_name": "Williams", "phone": "555-123-4567", "email": "bob.williams@example.com"},
    {"first_name": "Emma", "last_name": "Brown", "email": "emma.brown@example.com"},
    {"first_name": "Michael", "last_name": "Davis", "phone": "777-888-9999", "email": "michael.davis@example.com"},
    {"first_name": "Olivia", "last_name": "Miller", "phone": "111-222-3333", "email": "olivia.miller@example.com"},
    {"first_name": "David", "last_name": "Wilson", "email": "david.wilson@example.com"},
    {"first_name": "Sophia", "last_name": "Moore", "phone": "444-555-6666", "email": "sophia.moore@example.com"},
    {"first_name": "James", "last_name": "Taylor", "email": "james.taylor@example.com"},
    {"first_name": "Emily", "last_name": "Anderson", "phone": "888-999-0000", "email": "emily.anderson@example.com"},
    {"first_name": "William", "last_name": "Thomas", "email": "william.thomas@example.com"},
    {"first_name": "Ava", "last_name": "Jackson", "phone": "222-333-4444", "email": "ava.jackson@example.com"},
    {"first_name": "Daniel", "last_name": "White", "phone": "666-777-8888", "email": "daniel.white@example.com"},
    {"first_name": "Mia", "last_name": "Harris", "email": "mia.harris@example.com"},
    {"first_name": "Joseph", "last_name": "Martin", "phone": "999-000-1111", "email": "joseph.martin@example.com"},
    {"first_name": "Charlotte", "last_name": "Thompson", "email": "charlotte.thompson@example.com"},
    {"first_name": "Christopher", "last_name": "Garcia", "phone": "333-444-5555", "email": "christopher.garcia@example.com"},
    {"first_name": "Amelia", "last_name": "Martinez", "phone": "777-666-5555", "email": "amelia.martinez@example.com"},
    {"first_name": "Andrew", "last_name": "Robinson", "email": "andrew.robinson@example.com"}
]

# Create and save contacts using a loop
for data in contacts_data:
    contact = Contact(**data)
    contact.save()
                
@app.route("/")
def index():
    return redirect("/contacts")

@app.route("/contacts", methods=["GET"])
def contacts():
    search = request.args.get("q")
    page = int(request.args.get("page", 1))
    if search is not None:
        contacts_set = Contact.search(search)
        if request.headers.get('HX-Trigger') == 'search':
            print(contacts_set)
            return render_template("rows.html", contacts=contacts_set)
    else:
        contacts_set = Contact.all(page)    
    return render_template("index.html", contacts=contacts_set, page=page)

@app.route("/contacts/count")
def contacts_count():
    count = Contact.count()
    return "(" + str(count) + " total Contacts)"

@app.route("/contacts", methods=["POST"])
def contacts_post():
    search = request.form["q"]
    if search is not None:
        contacts_set = Contact.search(search)
    else:
        contacts_set = Contact.all()    
    return render_template("index.html", contacts=contacts_set)

@app.route("/contacts/new", methods=["GET"])
def contacts_new_get():
    return render_template("new.html", contact=Contact())

@app.route("/contacts/new", methods=["POST"])
def contacts_new():
    c = Contact(
        request.form["first_name"],
        request.form["last_name"],
        request.form["phone"],
        request.form["email"]
    )

    if c.save():
        flash("Created new contact")
        print(c.all())
        return redirect("/contacts")
    else:
        return render_template("new.html", contact = c)
    
@app.route("/contacts/<contact_id>", methods=["GET"])
def contacts_view(contact_id=0):
    contact = Contact.find(contact_id)

    if (contact is None):
        return redirect('/contacts')

    return render_template("show.html", contact = contact)

@app.route("/contacts/<contact_id>/edit", methods=["GET"])
def contacts_edit(contact_id=0):
    contact = Contact.find(contact_id)

    if (contact is None):
        return redirect('/contacts')
    
    return render_template("edit.html", contact=contact)

@app.route("/contacts/<contact_id>/edit", methods=["POST"])
def contacts_edit_post(contact_id=0):
    c = Contact.find(contact_id)
    c.update(
        first = request.form['first_name'],
        last = request.form['last_name'],
        email = request.form['email'],
        phone = request.form['phone']
    )

    if c.save():
        flash("Updated Contact!")
        return redirect("/contacts/" + str(contact_id))
    else:
        return render_template('edit.html', contact = c)
    
@app.route("/contacts/<contact_id>/email", methods=["GET"])
def contacts_email_get(contact_id=0):
    c = Contact.find(contact_id)
    c.email = request.args.get("email")
    c.validate()
    return c.errors.get("email") or ""

@app.route("/contacts/<contact_id>", methods=["DELETE"])
def contacts_delete(contact_id=0):
    Contact.delete(contact_id) 
    if request.headers.get('HX-Trigger') == 'delete-btn':
        flash("Deleted Contact!")
        return redirect("/contacts", 303)
    else:
        return ""
    
@app.route("/contacts", methods=["DELETE"])
def contacts_delete_all():
    contact_ids = [
        id
        for id in request.form.getlist("selected_contact_ids")
    ]
    for contact_id in contact_ids:
        print(contact_id)
        print(Contact.delete(contact_id))
    flash("Deleted contacts!")
    contacts_set = Contact.all()
    return render_template("index.html", contacts=contacts_set, page=0)
    