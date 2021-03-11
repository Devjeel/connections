from http import HTTPStatus

from tests.factories import PersonFactory


def test_mutual_friends(db, testapp):
    person_from1 = PersonFactory()
    person_from2 = PersonFactory()

    # Both person will be connected to person_from, making it mutual for both.
    person_to1 = PersonFactory()
    person_to2 = PersonFactory()
    # Commit persons
    db.session.commit()

    person_from_ids = [person_from1.id, person_from2.id]
    person_to_ids = [person_to1.id, person_to2.id]

    for person_from_id in person_from_ids:
        for person_to_id in person_to_ids:
            json_connection = {
                'from_person_id': person_from_id,
                'to_person_id': person_to_id,
                'connection_type': 'coworker',
            }

            # Need to send json load; ConnectionFactory needs debugging
            testapp.post('/connections', json=json_connection)

    # assert mutual relations
    res = testapp.get(f'/connections/{person_from1.id}/mutual_friends?target_id={person_from2.id}')
    assert res.status_code == HTTPStatus.OK
    assert len(res.json) == 2  # manually counted

    # Result will be the same set of data if you swap person_id and target_id
    res = testapp.get(f'/connections/{person_from2.id}/mutual_friends?target_id={person_from1.id}')
    assert res.status_code == HTTPStatus.OK
    assert len(res.json) == 2  # manually counted

    # To persons are mutual and should match ids
    for result in res.json:
        assert result['id'] in person_to_ids
