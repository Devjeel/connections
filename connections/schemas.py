from datetime import datetime

from marshmallow import fields, validate, validates, validates_schema, ValidationError
from marshmallow_enum import EnumField

from connections.extensions import ma
from connections.models.connection import Connection, ConnectionType
from connections.models.person import Person


class BaseModelSchema(ma.ModelSchema):
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)


class PersonSchema(BaseModelSchema):
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str(required=True, validate=validate.Email(error='Not a valid email address.'))
    date_of_birth = fields.Str()

    @validates('date_of_birth')
    def validate_date_of_birth(self, date_of_birth):
        # 0000-00-00 is just an invalid date and wont be converted to a datetime object
        if date_of_birth == '0000-00-00':
            raise ValidationError('Not a valid date.')

        now_date = datetime.now()

        # convert inserted time from str to datetime, tests are using y-m-d format
        date_of_birth_obj = datetime.strptime(date_of_birth, '%Y-%m-%d')
        if date_of_birth_obj > now_date:
            raise ValidationError('Cannot be in the future.')

    class Meta:
        model = Person


class ConnectionSchema(BaseModelSchema):
    from_person_id = fields.Integer()
    to_person_id = fields.Integer()
    connection_type = EnumField(ConnectionType)

    @validates_schema
    def validate_age(self, data, **kwargs):
        # only validates age if its a parent to child connection
        connection_name = data['connection_type'].name

        # from parent to child
        if connection_name == 'mother' or connection_name == 'father':
            parent = Person.query.filter_by(id=data['from_person_id']).first()
            child = Person.query.filter_by(id=data['to_person_id']).first()

            if parent.date_of_birth >= child.date_of_birth:
                raise ValidationError(f'Invalid connection - {connection_name} younger than child.')

        # from child to parent
        elif connection_name == 'son' or connection_name == 'daughter':
            parent = Person.query.filter_by(id=data['to_person_id']).first()
            child = Person.query.filter_by(id=data['from_person_id']).first()

            if parent.date_of_birth >= child.date_of_birth:
                raise ValidationError(f'Invalid connection - {connection_name} older than parent.')

    class Meta:
            model = Connection
