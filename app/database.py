import sqlite3
from typing import Any
from contextlib import contextmanager

from app.schemas import ShipmentCreate, ShipmentUpdate


class Database:

    def connect_to_db(self):
        # Make connection
        self.connection = sqlite3.connect("shipments.db", check_same_thread=False)
        # Get cursor to execute queries and fetch data
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS shipment (id INTEGER PRIMARY KEY, content TEXT, weight REAL, status TEXT)",
        )

    def create(self, shipment: ShipmentCreate) -> int:
        # Find a new id
        self.cursor.execute("SELECT MAX(id) FROM shipment")
        result = self.cursor.fetchone()

        new_id = (result[0] or 0) + 1

        self.cursor.execute(
            "INSERT INTO shipment VALUES (:id, :content, :weight, :status)",
            {"id": new_id, **shipment.model_dump(), "status": "placed"},
        )

        self.connection.commit()

        return new_id

    def get(self, id: int) -> dict[str, Any] | None:
        self.cursor.execute(
            "SELECT * FROM shipment WHERE id = :id",
            {"id": id},
        )
        row = self.cursor.fetchone()

        return (
            {"id": row[0], "content": row[1], "weight": row[2], "status": row[3]}
            if row
            else None
        )

    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any]:
        self.cursor.execute(
            "UPDATE shipment SET status = :status WHERE id = :id",
            {"id": id, **shipment.model_dump()},
        )

        self.connection.commit()

        return self.get(id)  # type: ignore

    def delete(self, id: int):
        self.cursor.execute("DELETE FROM shipment WHERE id = ?", (id,))

        self.connection.commit()

    def close(self):
        self.connection.close()

    # def __enter__(self):
    #     self.connect_to_db()
    #     self.create_table()
    #     return self

    # def __exit__(self, *arg):
    #     self.close()


@contextmanager
def managed_db():
    db = Database()
    db.connect_to_db()
    db.create_table()

    yield db

    db.close()


# SQL Model
with managed_db() as db:
    print(db.get(12701))
    print(db.get(12702))
