import unittest
import os
import json
from library import Book, Library


class TestBook(unittest.TestCase):
    """Класс для тестирования функциональности класса Book."""

    def test_to_dict(self):
        """Тестирует метод to_dict класса Book."""
        book = Book(1, 'Test Title', 'Test Author', 2020, 'в наличии')
        self.assertEqual(book.to_dict(), {
            'id': 1,
            'title': 'Test Title',
            'author': 'Test Author',
            'year': 2020,
            'status': 'в наличии'
        })

    def test_from_dict(self):
        """Тестирует метод from_dict класса Book."""
        data = {
            'id': 1,
            'title': 'Test Title',
            'author': 'Test Author',
            'year': 2020,
            'status': 'в наличии'
        }
        book = Book.from_dict(data)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, 'Test Title')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.year, 2020)
        self.assertEqual(book.status, 'в наличии')


class TestLibrary(unittest.TestCase):
    """Класс для тестирования функциональности класса Library."""

    def setUp(self):
        """Настраивает тестовую среду перед каждым тестом."""
        self.library = Library('test_library.json')

    def tearDown(self):
        """Очищает тестовую среду после каждого теста."""
        if os.path.exists('test_library.json'):
            os.remove('test_library.json')

    def test_add_book(self):
        """Тестирует метод add_book класса Library."""
        book = self.library.add_book('Test Title', 'Test Author', 2020)
        self.assertEqual(book.title, 'Test Title')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.year, 2020)
        self.assertEqual(book.status, 'в наличии')
        self.assertTrue(os.path.exists('test_library.json'))

    def test_remove_book(self):
        """Тестирует метод remove_book класса Library."""
        book = self.library.add_book('Test Title', 'Test Author', 2020)
        self.assertTrue(self.library.remove_book(book.id))
        self.assertFalse(self.library.remove_book(book.id))

    def test_find_books(self):
        """Тестирует метод find_books класса Library."""
        self.library.add_book('Test Title', 'Test Author', 2020)
        self.library.add_book('Another Title', 'Another Author', 2021)

        results = self.library.find_books(title='Test Title')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Test Title')

        results = self.library.find_books(author='Another Author')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, 'Another Author')

        results = self.library.find_books(year=2020)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].year, 2020)

    def test_list_books(self):
        """Тестирует метод list_books класса Library."""
        self.library.add_book('Test Title', 'Test Author', 2020)
        self.library.add_book('Another Title', 'Another Author', 2021)

        books = self.library.list_books()
        self.assertEqual(len(books), 2)

    def test_update_status(self):
        """Тестирует метод update_status класса Library."""
        book = self.library.add_book('Test Title', 'Test Author', 2020)
        self.assertTrue(self.library.update_status(book.id, 'выдана'))
        self.assertEqual(self.library.find_books(
            title='Test Title')[0].status, 'выдана')
        self.assertFalse(self.library.update_status(999, 'в наличии'))


if __name__ == '__main__':
    unittest.main()
