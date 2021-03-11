from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model
from connections.models.connection import Connection


class Person(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    connections = db.relationship('Connection', foreign_keys='Connection.from_person_id')

    def format(self):
        # return a dictionary to be converted to json by the route endpoint.
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'date_of_birth': self.date_of_birth,
        }

    """
    returns an array of mutual connections between this instance and a target instance
    target_id is the id of the target person that we are going to check for mutual connections
    """
    def mutual_friends(self, target_id):

        # plan: loop through each one of the main person connection. and check if target_person
        # is also a connection, if yes and it's not target id then thats a mutual

        # get all instance person connections
        instance_connected_people_ids = self.get_all_connections_by_id(self.id)

        print([con for (con,) in instance_connected_people_ids])
        # get all target  person connections
        target_connected_people_ids = self.get_all_connections_by_id(target_id)

        mutual_connections = []

        # loop through the instance person connections
        for (connected_person_id,) in instance_connected_people_ids:
            # check if this current instance person connection id is also available in the target
            # connections ids
            if any(
                target_connected_people_id == connected_person_id for (target_connected_people_id,)
                    in target_connected_people_ids):

                # if this common connection isn't the same person id then its a mutual
                if connected_person_id != self.id:
                    person = Person.query.filter_by(id=connected_person_id).first()
                    mutual_connections.append(person)

        return mutual_connections

    def get_all_connections_by_id(self, id):
        # filter by ids only
        return Connection.query.with_entities(Connection.to_person_id).filter(
            (Connection.from_person_id == self.id) | (Connection.to_person_id == self.id)).all()
