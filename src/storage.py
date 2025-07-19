import pickle
from models import AddressBook, NoteBook


def save_data(obj):
    if isinstance(obj, AddressBook):
        filename = "addressbook.pkl"
    elif isinstance(obj, NoteBook):
        filename = "notebook.pkl"
    else:
        raise TypeError("Unsupported object type for saving")

    with open(filename, "wb") as f:
        pickle.dump(obj, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def load_notebook(filename="notebook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NoteBook()
