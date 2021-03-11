from http import HTTPStatus

from tests.factories import PersonFactory

EXPECTED_FIELDS = [
    'id',
    'from_person_id',
    'to_person_id',
    'connection_type',
]


def test_can_get_connections(db, testapp):

    # TODO: fix the create_batch for the connection factory class

    person_from1 = PersonFactory(first_name='Jeel')
    person_to1 = PersonFactory(first_name='Patel')

    person_from2 = PersonFactory(first_name='sky')
    person_to2 = PersonFactory(first_name='blue')
    db.session.commit()

    json_connection1 = {
        'from_person_id': person_from1.id,
        'to_person_id': person_to1.id,
        'connection_type': 'coworker',
    }

    json_connection2 = {
        'from_person_id': person_from2.id,
        'to_person_id': person_to2.id,
        'connection_type': 'coworker',
    }
    res = testapp.post('/connections', json=json_connection1)
    res = testapp.post('/connections', json=json_connection2)

    res = testapp.get('/connections')

    assert res.status_code == HTTPStatus.OK
    assert len(res.json) == 2

    # assert that the person objects are also included
    assert res.json[0]['from_person']['id'] == person_from1.id
    assert res.json[0]['to_person']['id'] == person_to1.id
