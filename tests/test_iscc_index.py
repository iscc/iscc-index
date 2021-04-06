from iscc_index import __version__
from fastapi.testclient import TestClient
from iscc_index.main import app
import iscc


client = TestClient(app)


def test_version():
    assert __version__ == "1.1.0-beta.4"


def test_add_simple():
    with TestClient(app) as client:
        code = iscc.Code.rnd(iscc.MT.ISCC, bits=256).code
        result = client.post("/add", json={"iscc": code})
        assert result.json() == {"added": 0}
        app.state.index.close()
        app.state.index.destroy()


def test_query_simple():
    with TestClient(app) as client:
        code = iscc.Code.rnd(iscc.MT.ISCC, bits=256).code
        client.post("/add", json={"iscc": code})
        result = client.post("/query", json={"iscc": code})
        assert result.json() == {
            "feature_matches": [],
            "iscc_matches": [
                {
                    "cdist": 0,
                    "ddist": 0,
                    "distance": 0,
                    "imatch": True,
                    "key": "0",
                    "matched_iscc": code,
                    "mdist": 0,
                }
            ],
        }
        app.state.index.close()
        app.state.index.destroy()


def test_stats_simple():
    with TestClient(app) as client:
        code = iscc.Code.rnd(iscc.MT.ISCC, bits=256).code
        client.post("/add", json={"iscc": code})
        result = client.get("/stats")
        assert result.json().get("isccs") == 1
        app.state.index.close()
        app.state.index.destroy()
