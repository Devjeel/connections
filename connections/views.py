from http import HTTPStatus

from flask import abort, Blueprint, jsonify, request
from webargs.flaskparser import use_args

from connections.models.connection import Connection, ConnectionType
from connections.models.person import Person
from connections.schemas import ConnectionSchema, PersonSchema

blueprint = Blueprint('connections', __name__)


@blueprint.route('/', methods=['GET'])
def index():
    return 'Connections project!', HTTPStatus.OK


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['GET'])
def get_connections():
    connections = Connection.query.all()  # all available connections

    json_data = []  # to be filled with json data.

    # loop through each connection, fetch and format it and its related people and
    # append to the json_data array
    for connection in connections:
        connection_json = connection.format()

        from_person = Person.query.filter_by(id=connection.from_person_id).first()
        connection_json['from_person'].update(from_person.format())

        to_person = Person.query.filter_by(id=connection.to_person_id).first()
        connection_json['to_person'].update(to_person.format())

        json_data.append(connection_json)

    return jsonify(json_data), HTTPStatus.OK


@blueprint.route('/connections/<int:id>', methods=['PATCH'])
def edit_connections(id):
    edited_connection = request.get_json()
    validate_type(edited_connection['type'])

    connection = Connection.query.filter_by(id=id).first()

    edited_connection = connection.update_type(edited_connection['type'])

    return jsonify(edited_connection), HTTPStatus.OK


@blueprint.route('/connections/<int:id>/mutual_friends', methods=['GET'])
def get_mutual_connections(id):
    target_person_id = request.args.get('target_id', None)
    mutual_connections = []

    if target_person_id:
        instance_person = Person.query.filter_by(id=id).first()

        mutual_connections = instance_person.mutual_friends(target_person_id)

    # Can also use PersonSchema to return data
    return jsonify([person.format() for person in mutual_connections]), HTTPStatus.OK


def validate_type(type):
    # loop through the existing types enum, if found return true else abort.

    for allowed_type in ConnectionType:

        if allowed_type.name == type:
            return True

    abort(403)  # raising unprocessable_entity error.
