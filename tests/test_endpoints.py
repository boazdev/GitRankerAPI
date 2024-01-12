import time
from fastapi.testclient import TestClient
import pytest
from app.main import app
class TestFiles:
    """ def __init__(self):
        self.ticket_validator = TypeAdapter(TicketModel) """
    @pytest.fixture(autouse=True)
    def setup(self):
        # Perform setup actions here (e.g., creating resources, setting up connections)
        self.client = TestClient(app)


    def test_create_user(self):
        for i in range(100):
            time.sleep(1)
            response = self.client.post("/users_metadata/users", json={
    "apiKey": "00069cf7-aa5d-4ffb-925b-2077bdc83288",
    "userMetaData": {
        "userName": "testuser123",
        "name": "testuser123",
        "commits": 1+i,
        "stars": 2+i,
        "forks": 3+i,
        "linesCode": 4+i,
        "linesTests": 5+i,
        "followers": 6,
        "following": 7,
        "publicRepos": 8,
        "emptyRepos": 2,
        "forkedRepos": 3
    },
    "linesByLanguages": {
        "java": 200,
        "py": 400,
        "js": 700,
        "php": 0,
        "rb": 0,
        "cpp": 0,
        "h": 0,
        "c": 0,
        "cs": 0,
        "html": 0,
        "ipynb": 0,
        "css": 0,
        "ts": 0,
        "kt": 0,
        "dart": 0,
        "m": 0,
        "swift": 0,
        "go": 0,
        "rs": 0,
        "scala": 0,
        "scss": 0,
        "asm": 0,
        "pwn": 0,
        "inc": 0,
        "scss_repositories": 0,
        "assembly_repositories": 0,
        "pawn_repositories": 0,
        "objectivec_repositories": 0,
        "kotlin_repositories": 0,
        "dart_repositories": 0,
        "c_repositories": 0,
        "typescript_repositories": 0,
        "html_repositories": 0,
        "java_repositories": 0,
        "ejs_repositories": 0,
        "csharp_repositories": 0,
        "javascript_repositories": 0,
        "jupyter_repositories": 0,
        "cpp_repositories": 0,
        "css_repositories": 0,
        "python_repositories": 0,
        "nodejs_repositories": 0,
        "angular_repositories": 0,
        "react_repositories": 0,
        "dotnet_repositories": 0,
        "php_repositories": 0,
        "ruby_repositories": 0,
        "scala_repositories": 0,
        "swift_repositories": 0,
        "go_repositories": 0,
        "r_repositories": 0,
        "rust_repositories": 0,
        "users_metadata_id": 0
    }
    })
        assert response.status_code == 201
        #assert response.json()["username"] == "testuser123"