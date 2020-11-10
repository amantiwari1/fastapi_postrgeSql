from fastapi.testclient import TestClient

from main import app

client = TestClient(app)



def test_read_main():
    '''
    If you want to build and push the docker image then type 'yes'
    else type 'no'
    '''
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "yes"} # yes or no 