import pytest
from fastapi.testclient import TestClient

from main import DB_PROVIDER, app
from src.applications import ReadMindMapApps, ReadMindMapApp, \
    CreateMindMapApp, ReadMindMapAppsPrettyFormat
from src.models import MindMapLeaf, MindMapAppCreateError, \
    MindMapApp
from src.providers import MindMapDBProvider


class TestMindMapModels:

    def test_mind_map_app(self):
        data = {
            "id": "fake-app-0",
            "data": []
        }
        mind_map_app = MindMapApp(**data)
        assert mind_map_app.id == data['id']
        assert mind_map_app.data == data['data']

    def test_mind_map_leaf(self):
        data = {
            "path": "/fake/this/is/a/path/0",
            "text": "This is a fake topic 0",
        }
        mind_map_leaf = MindMapLeaf(**data)
        assert mind_map_leaf.path == data['path']
        assert mind_map_leaf.text == data['text']

    def test_mind_map_app_with_leaf(self):
        data = {
            "id": "fake-app-0",
            "data": [
                {
                    "path": "fake/i/like/potatoes",
                    "text": "Because fake reasons"
                },
                {
                    "path": "/this/is/a/path/1",
                    "text": "This is a sample topic 1"
                }
            ]
        }
        mind_map_app = MindMapApp(**data)
        assert mind_map_app.id == data['id']
        assert mind_map_app.data == data['data']


class TestMindMapProviders:
    DB = MindMapDBProvider()
    sample = [
        {
            "id": "fake-app-0",
            "data": [
                {
                    "path": "fake/i/like/potatoes",
                    "text": "Because fake reasons"
                },
                {
                    "path": "/this/is/a/path/1",
                    "text": "This is a sample topic 1"
                }
            ]

        },
        {
            "id": "fake-app-1",
            "data": [
                {
                    "path": "fake/i/like/potatoes",
                    "text": "Because fake reasons"
                },
                {
                    "path": "/this/is/a/path/1",
                    "text": "This is a sample topic 1"
                }
            ]

        },
    ]
    DB.db = sample

    def test_read_mind_map_apps(self):
        mind_map_apps = self.DB.read_mind_map_apps()
        assert mind_map_apps[0].dict() == {
            'id': 'fake-app-0',
            'data': [
                {
                    'path': 'fake/i/like/potatoes',
                    'text': 'Because fake reasons'
                },
                {
                    'path': '/this/is/a/path/1',
                    'text': 'This is a sample topic 1'
                }
            ]}

    def test_read_mind_map_apps_empty_list(self):
        self.DB.db = []
        mind_map_apps = self.DB.read_mind_map_apps()
        self.DB.db = self.sample
        assert mind_map_apps == []

    def test_read_mind_map_app(self):
        mind_map_app_ok = self.DB.read_mind_map_app(id="fake-app-0")
        mind_map_app_none = self.DB.read_mind_map_app(id="foo")
        assert mind_map_app_ok.dict() == self.sample[0]
        assert mind_map_app_none is None

    def test_create_mind_map_app(self):
        data = {
            "id": "app-3",
        }
        new_mind_map_app = MindMapApp(**data)
        mind_map_leaf = self.DB.create_mind_map_app(
            mind_map_app=new_mind_map_app)
        assert isinstance(mind_map_leaf, MindMapApp)
        assert mind_map_leaf.dict() == {
            "id": "app-3",
            "data": []
        }

    def test_create_mind_map_app_already_exist(self):
        data = {
            "id": "fake-app-0",
        }
        new_mind_map_app = MindMapApp(**data)
        with pytest.raises(MindMapAppCreateError):
            self.DB.create_mind_map_app(mind_map_app=new_mind_map_app)

    def test_add_mind_map_app(self):
        leaf = {
            'path': "fake/i/hate/apple",
            'text': 'Because bad reasons'
        }

        mind_map_leaf = MindMapLeaf(**leaf)
        mind_map_app = self.DB.add_mind_map_leaf(
            id="fake-app-0",
            mind_map_leaf=mind_map_leaf)

        assert mind_map_app.dict() == {
            'id': 'fake-app-0',
            'data': [
                {
                    'path': 'fake/i/like/potatoes',
                    'text': 'Because fake reasons'
                },
                {
                    'path': '/this/is/a/path/1',
                    'text': 'This is a sample topic 1'
                },
                {
                    'path': 'fake/i/hate/apple',
                    'text': 'Because bad reasons'
                }
            ]
        }


class TestMindMapApplications:
    DB = MindMapDBProvider()
    sample = [
        {
            "id": "fake-app-0",
            "data": [
                {
                    "path": "fake/i/like/potatoes",
                    "text": "Because fake reasons"
                },
                {
                    "path": "/this/is/a/path/1",
                    "text": "This is a sample topic 1"
                }
            ]

        },
        {
            "id": "fake-app-1",
            "data": [
                {
                    "path": "fake/i/like/potatoes",
                    "text": "Because fake reasons"
                },
                {
                    "path": "/this/is/a/path/1",
                    "text": "This is a sample topic 1"
                }
            ]

        },
    ]
    DB.db = sample

    def test_apps_read_mind_map_apps_pretty_format(self):
        mind_map_apps = ReadMindMapAppsPrettyFormat(db_provider=self.DB)()
        assert mind_map_apps[0] == {
            'id': 'fake-app-0',
            'data': [
                {
                    'path': ['fake', 'i', 'like', 'potatoes'],
                    'text': 'Because fake reasons'
                },
                {
                    'path': ['this', 'is', 'a', 'path', '1'],
                    'text': 'This is a sample topic 1'
                }
            ]
        }

    def test_apps_read_mind_map_apps(self):
        mind_map_apps = ReadMindMapApps(db_provider=self.DB)()
        assert mind_map_apps[0].dict() == {
            'id': 'fake-app-0',
            'data': [
                {
                    'path': 'fake/i/like/potatoes',
                    'text': 'Because fake reasons'
                },
                {
                    'path': '/this/is/a/path/1',
                    'text': 'This is a sample topic 1'
                }
            ]}

    def test_apps_read_mind_map_apps_empty_list(self):
        self.DB.db = []
        mind_map_apps = ReadMindMapApps(db_provider=self.DB)()
        self.DB.db = self.sample
        assert mind_map_apps == []

    def test_apps_read_mind_map_app(self):
        mind_map_app_ok = ReadMindMapApp(db_provider=self.DB)(id="fake-app-0")
        mind_map_app_none = ReadMindMapApp(db_provider=self.DB)(id="foo")
        assert mind_map_app_ok.dict() == self.sample[0]
        assert mind_map_app_none is None

    def test_apps_create_mind_map_app(self):
        data = {
            "id": "app-3",
        }
        new_mind_map_app = MindMapApp(**data)
        mind_map_leaf = CreateMindMapApp(db_provider=self.DB)(
            mind_map_app=new_mind_map_app)
        assert isinstance(mind_map_leaf, MindMapApp)
        assert mind_map_leaf.dict() == {
            "id": "app-3",
            "data": [],
        }

    def test_apps_create_mind_map_app_already_exist(self):
        data = {
            "id": "fake-app-0",
        }
        new_mind_map_app = MindMapApp(**data)
        with pytest.raises(MindMapAppCreateError):
            CreateMindMapApp(db_provider=self.DB)(
                mind_map_app=new_mind_map_app)


class TestMindMapAPI:
    sample = [
        {
            "id": "fake-app-0",
            "data": [
                {
                    "path": "fake/i/like/potatoes",
                    "text": "Because fake reasons"
                },
                {
                    "path": "/this/is/a/path/1",
                    "text": "This is a sample topic 1"
                }
            ]

        },
        {
            "id": "fake-app-1",
            "data": [
                {
                    "path": "fake/i/like/potatoes",
                    "text": "Because fake reasons"
                },
                {
                    "path": "/this/is/a/path/1",
                    "text": "This is a sample topic 1"
                }
            ]

        },
    ]
    DB_PROVIDER.db = sample
    client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.headers['content-type'] == 'text/html; charset=utf-8'

    def test_read_apps(self):
        response = self.client.get("/apps")
        assert response.status_code == 200
        assert response.json() == self.sample

    def test_read_app(self):
        response = self.client.get("/apps/fake-app-0")
        assert response.status_code == 200
        assert response.json() == self.sample[0]

    def test_create_app(self):
        response = self.client.post(
            "/apps/",
            json={
                "id": "apps-3"
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": "apps-3",
            "data": [],
        }

    def test_create_app_already_exists(self):
        response = self.client.post(
            "/apps/",
            json={
                "id": "fake-app-0"
            },
        )
        assert response.status_code == 404

    def test_add_leaf(self):
        response = self.client.put(
            "/apps/fake-app-0",
            json={
                "path": "a/new/path",
                "text": "a new text"
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": "fake-app-0",
            "data": [
                {
                    "path": "fake/i/like/potatoes",
                    "text": "Because fake reasons"
                },
                {
                    "path": "/this/is/a/path/1",
                    "text": "This is a sample topic 1"
                },
                {
                    "path": "a/new/path",
                    "text": "a new text"
                }
            ],
        }

    def test_add_leaf_invalid_id(self):
        response = self.client.put(
            "/apps/fake-app-999",
            json={
                "path": "a/new/path",
                "text": "a new text"
            },
        )
        assert response.status_code == 404
