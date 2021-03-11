import enum

from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model


class ConnectionType(enum.Enum):
    mother = 'mother'
    father = 'father'
    son = 'son'
    daughter = 'daughter'
    husband = 'husband'
    wife = 'wife'
    brother = 'brother'
    sister = 'sister'
    friend = 'friend'
    coworker = 'coworker'


class Connection(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    from_person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    to_person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    connection_type = db.Column(db.Enum(ConnectionType), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'connection_type': self.connection_type.name,
            'from_person_id': self.from_person_id,
            'from_person': {},
            'to_person_id': self.to_person_id,
            'to_person': {}
        }

    def update_type(self, new_type):
        self.connection_type = new_type

        try:
            db.session.commit()
            return self.format()
        except Exception:
            # raise error
            print('error')

        finally:
            db.session.close()
