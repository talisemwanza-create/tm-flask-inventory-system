import unittest
from app import app, inventory

class InventoryTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        inventory.clear()

    def test_home(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_get_inventory_empty(self):
        r = self.client.get('/inventory')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json, {})

    def test_add_and_get_item(self):
        r = self.client.post('/inventory', json={"barcode":"123","name":"Test","quantity":2})
        self.assertEqual(r.status_code, 201)
        r = self.client.get('/inventory')
        self.assertIn("123", r.json)

    def test_update_item(self):
        self.client.post('/inventory', json={"barcode":"123","quantity":1})
        r = self.client.put('/inventory/123', json={"quantity":10})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json['quantity'], 10)

    def test_delete_item(self):
        self.client.post('/inventory', json={"barcode":"123","quantity":1})
        r = self.client.delete('/inventory/123')
        self.assertEqual(r.status_code, 204)

    def test_lookup_external_api(self):
        r = self.client.get('/lookup/3017620422003')
        self.assertEqual(r.status_code, 200)
        self.assertIn("name", r.json)

if __name__ == '__main__':
    unittest.main()