from flask import Flask, jsonify, request
import mysql.connector

items = [
    {
        "id": 1,
        "name": "Margherita Pizza",
        "description": "Classic pizza topped with fresh tomatoes, mozzarella cheese, and basil.",
        "price": 12.99,
        "available": True,
    },
    {
        "id": 2,
        "name": "Caesar Salad",
        "description": "Crisp romaine lettuce, Parmesan cheese, croutons, and Caesar dressing.",
        "price": 8.99,
        "available": True,
    },
    {
        "id": 3,
        "name": "Grilled Chicken Sandwich",
        "description": "Grilled chicken breast with lettuce, tomato, and mayo on a toasted bun.",
        "price": 10.99,
        "available": False,
    },
    {
        "id": 4,
        "name": "Spaghetti Bolognese",
        "description": "Classic Italian pasta with a rich and savory meat sauce.",
        "price": 14.99,
        "available": True,
    },
    {
        "id": 5,
        "name": "Vegetable Stir-fry",
        "description": "Mixed vegetables sautéed in a flavorful soy-based sauce, served with rice.",
        "price": 11.49,
        "available": True,
    },
    {
        "id": 6,
        "name": "Beef Tacos",
        "description": "Three soft tacos filled with seasoned beef, lettuce, cheese, and salsa.",
        "price": 9.99,
        "available": True,
    },
    {
        "id": 7,
        "name": "Chocolate Lava Cake",
        "description": "Decadent chocolate cake with a molten chocolate center, served with vanilla ice cream.",
        "price": 6.99,
        "available": False,
    },
]

config = {
    "user": "root",
    "password": "root",
    "host": "localhost:3306",
    "database": "piotr",
    "raise_on_warnings": True,
}


app = Flask(__name__)


def get_connection():
    conn = mysql.connector.connect(
        user="root",
        password="root",
        host="localhost",
        port=3306,
        database="piotr",
        raise_on_warnings=False,
    )
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS food (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                description VARCHAR(150),
                price DECIMAL(10, 2),
                availability TINYINT
            )
            """
    )
    conn.commit()
    conn.close()


class Food:
    def __init__(self, id, name, description, price, availability):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.availability = availability

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "availability": self.availability,
        }


@app.route("/foods/")
def main_menu():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM food")
    rows = cursor.fetchall()
    foods = [
        Food(
            row["id"],
            row["name"],
            row["description"],
            row["price"],
            row["availability"],
        )
        for row in rows
    ]
    return jsonify([food.to_dict() for food in foods])


@app.route("/foods/", methods=["POST"])
def add_food():
    conn = get_connection()
    cursor = conn.cursor()
    data = request.json
    new_food = Food(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        availability=data["availability"],
    )
    cursor.execute(
        "INSERT INTO food(name,description,price,availability) VALUES(%s,%s,%s,%s)",
        (
            new_food.name,
            new_food.description,
            new_food.price,
            new_food.availability,
        ),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    app.run(debug=True)


new_foods = []


# for item in items:
#     new_food = Food(
#         item["id"], item["name"], item["description"], item["price"], item["available"]
#     )
#     new_foods.append(new_food)

# for food in new_foods:
#     print(food)
