import json
import os
from typing import List, Optional, Dict


class Book:
    """Класс для представления книги."""

    def __init__(self, book_id: int, title: str, author: str,
                 year: int, status: str = 'в наличии'):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict[str, str]:
        """Преобразует объект книги в словарь."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @staticmethod
    def from_dict(data: Dict[str, str]) -> 'Book':
        """Создает объект книги из словаря."""
        return Book(data['id'], data['title'],
                    data['author'], data['year'], data['status'])


class Library:
    """Класс для управления библиотекой книг."""

    def __init__(self, datafile: str = 'library.json'):
        self.books: List[Book] = []
        self.datafile = datafile
        self._load_books()

    def _load_books(self):
        """Загружает книги из файла."""
        if os.path.exists(self.datafile):
            with open(self.datafile, 'r', encoding='utf-8') as file:
                books_data = json.load(file)
                self.books = [Book.from_dict(book) for book in books_data]

    def _save_books(self):
        """Сохраняет книги в файл."""
        with open(self.datafile, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books],
                      file, ensure_ascii=False, indent=4)

    def _generate_id(self) -> int:
        """Генерирует уникальный идентификатор для новой книги."""
        if not self.books:
            return 1
        return max(book.id for book in self.books) + 1

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Добавляет новую книгу в библиотеку."""
        book_id = self._generate_id()
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self._save_books()
        return new_book

    def remove_book(self, book_id: int) -> bool:
        """Удаляет книгу из библиотеки по идентификатору."""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self._save_books()
                return True
        return False

    def find_books(self, title: Optional[str] = None,
                   author: Optional[str] = None,
                   year: Optional[int] = None) -> List[Book]:
        """Ищет книги по названию, автору или году издания."""
        results = self.books
        if title is not None:
            results = [book for book in results if title.lower()
                       in book.title.lower()]
        if author is not None:
            results = [book for book in results if author.lower()
                       in book.author.lower()]
        if year is not None:
            results = [book for book in results if book.year == year]
        return results

    def list_books(self) -> List[Book]:
        """Возвращает список всех книг в библиотеке."""
        return self.books

    def update_status(self, book_id: int, status: str) -> bool:
        """Обновляет статус книги."""
        for book in self.books:
            if book.id == book_id:
                book.status = status
                self._save_books()
                return True
        return False


def main():
    """Основная функция для взаимодействия с пользователем."""
    library = Library()

    while True:
        print('\nСистема управления библиотекой')
        print('1. Добавить книгу')
        print('2. Удалить книгу')
        print('3. Найти книгу')
        print('4. Отобразить все книги')
        print('5. Изменить статус книги')
        print('0. Выйти')

        choice = input('Выберите действие: ')

        if choice == '1':
            title = input('Введите название книги: ')
            author = input('Введите автора книги: ')
            year = int(input('Введите год издания книги: '))
            book = library.add_book(title, author, year)
            print(f'Книга добавлена с id: {book.id}')
        elif choice == '2':
            book_id = int(input('Введите id книги для удаления: '))
            if library.remove_book(book_id):
                print('Книга удалена.')
            else:
                print('Книга не найдена.')
        elif choice == '3':
            title = input(
                'Введите название книги (оставьте пустым, если не нужно): ')
            author = input(
                'Введите автора книги (оставьте пустым, если не нужно): ')
            year = input(
                'Введите год издания книги (оставьте пустым, если не нужно): ')
            year = int(year) if year else None
            results = library.find_books(title or None, author or None, year)
            if results:
                for book in results:
                    print(book.to_dict())
            else:
                print('Книги не найдены.')
        elif choice == '4':
            books = library.list_books()
            for book in books:
                print(book.to_dict())
        elif choice == '5':
            book_id = int(input('Введите id книги: '))
            status = input('Введите новый статус книги (в наличии/выдана): ')
            if library.update_status(book_id, status):
                print('Статус книги обновлен.')
            else:
                print('Книга не найдена.')
        elif choice == '0':
            break
        else:
            print('Неверный выбор, попробуйте снова.')


if __name__ == '__main__':
    main()
