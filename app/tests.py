import os
import unittest

from app import create_app, db


class CityCarManagementAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Welcome to City Car Management API!'})

    def test_add_owner(self):
        response = self.client.post('/owners', json={'name': 'John Doe'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['name'], 'John Doe')

    def test_get_owners(self):
        self.client.post('/owners', json={'name': 'John Doe'})
        response = self.client.get('/owners')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json), 0)

    def test_add_car(self):
        owner_response = self.client.post('/owners', json={'name': 'Jane Doe'})
        owner_id = owner_response.json['id']
        response = self.client.post('/cars', json={'color': 'blue', 'model': 'hatch', 'owner_id': owner_id})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_cars(self):
        owner_response = self.client.post('/owners', json={'name': 'Jane Doe'})
        owner_id = owner_response.json['id']
        self.client.post('/cars', json={'color': 'blue', 'model': 'hatch', 'owner_id': owner_id})
        response = self.client.get('/cars')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json), 0)

    def test_sales_opportunities(self):
        owner_response = self.client.post('/owners', json={'name': 'Jack Doe'})
        owner_id = owner_response.json['id']
        response = self.client.get('/owners/sales_opportunities')
        self.assertEqual(response.status_code, 200)
        self.assertIn({'id': owner_id, 'name': 'Jack Doe'}, response.json)


if __name__ == '__main__':
    unittest.main()
