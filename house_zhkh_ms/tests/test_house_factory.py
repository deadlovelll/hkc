import unittest

from house_zhkh_ms.house_factory.house_factory import HouseFactory

class HouseFactoryTest(unittest.TestCase):
    
    """
    Test suite for the HouseFactory class.
    """
    
    def test_create_house (
        self,
    ) -> None:
        
        rows = [
            (1, 101, 'A1', 2, 50.0, 201, 'Water', 30.0, 301, '2024-02-01', 25.0, 401, 'John Doe', 30, 100.0),
            (1, 101, 'A1', 2, 50.0, 202, 'Gas', 15.0, None, None, None, None, None, None, None),
            (1, 102, 'B1', 3, 60.0, None, None, None, None, None, None, 402, 'Jane Doe', 28, 200.0)
        ]
        
        house = HouseFactory.create_house(rows)
        
        self.assertEqual(house['house_id'], 1)
        self.assertEqual(len(house['flats']), 2)
        self.assertIn('A1', house['flats'])
        self.assertIn('B1', house['flats'])
        
        flat_a1 = house['flats']['A1']
        self.assertEqual(flat_a1['flat_id'], 101)
        self.assertEqual(flat_a1['square'], 50.0)
        self.assertEqual(len(flat_a1['counters']), 2)
        self.assertEqual (
            flat_a1['counters'][0]['counter_type'], 
            'Water'
        )
        
        flat_b1 = house['flats']['B1']
        self.assertEqual(len(flat_b1['counters']), 0)
        self.assertEqual(len(flat_b1['inhabitants']), 1)
        self.assertEqual (
            flat_b1['inhabitants'][0]['full_name'], 
            'Jane Doe'
        )