from http import HTTPStatus

from tests.factories import PersonFactory

EXPECTED_FIELDS = [
    'id',
    'from_person_id',
    'to_person_id',
    'connection_type',
]


def test_can_change_connection_type(db, testapp):
    person_from = PersonFactory()
    person_to = PersonFactory()
    db.session.commit()

    json_connection = {
        'from_person_id': person_from.id,
        'to_person_id': person_to.id,
        'connection_type': 'coworker',
    }
    res = testapp.post('/connections', json=json_connection)

    json_connection_edit = {
        'type': 'sister',
    }
    res = testapp.patch(f'/connections/{res.json["id"]}',  json=json_connection_edit)

    assert res.status_code == HTTPStatus.OK
    assert res.json['connection_type'] == 'sister'


def test_gives_if_connect_type_not_allowed_gives_error(db, testapp):
    person_from = PersonFactory()
    person_to = PersonFactory()
    db.session.commit()

    json_connection = {
        'from_person_id': person_from.id,
        'to_person_id': person_to.id,
        'connection_type': 'coworker',
    }
    res = testapp.post('/connections', json=json_connection)

    json_connection_edit = {
        'type': 'not allowed',
    }

    res = testapp.patch(f'/connections/{res.json["id"]}',  json=json_connection_edit)

    assert res.status_code == 403
