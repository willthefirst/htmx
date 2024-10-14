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

    @classmethod
    def all(cls):
        return cls.contacts

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
    
# Instantiate some members of the Contact class
contact1 = Contact(first_name="John", last_name="Doe", phone="123-456-7890",  email="john.doe@example.com")
contact2 = Contact(first_name="Jane", last_name="Smith", email="jane.smith@example.com")
contact3 = Contact(first_name="Alice", last_name="Johnson", phone="098-765-4321", email="alice.johnson@example.com")

contact1.save()
contact2.save()
contact3.save()
                
@app.route("/")
def index():
    return redirect("/contacts")

@app.route("/contacts")
def contacts():
    search = request.args.get("q")
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

@app.route("/contacts/<contact_id>/delete", methods=["POST"])
def contacts_delete(contact_id=0):
    Contact.delete(contact_id) 
    flash("Deleted Contact!")
    return redirect("/contacts")