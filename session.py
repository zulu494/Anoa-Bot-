class Session(object):
    contacts = {}

    def set(self, contact, session = 0):
        self.contacts[contact] = session
        return session

    def get(self, contact):
        if contact not in self.contacts:
            self.set(contact)
        
        return self.contacts[contact]