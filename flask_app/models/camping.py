from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Camping:
    db_name = "camping"
    def __init__(self, data):
        self.id = data["id"]
        self.description = data["description"]
        self.image = data["image"]
        self.location = data["location"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def get_all_Campings(cls):
        query = "SELECT * FROM campings"
        result = connectToMySQL(cls.db_name).query_db(query)
        campings = []
        if result:
            for camping in result:
                campings.append(camping)
        return campings
        

    @classmethod
    def get_all_Cityis(cls):
        query = "SELECT * FROM cities"
        result = connectToMySQL(cls.db_name).query_db(query)
        campings = []
        if result:
            for camping in result:
                campings.append(camping)
        return campings

    @classmethod
    def create(cls, data):
        query = "INSERT INTO campings (description, image, location, user_id, city_id) VALUES (%(description)s, %(image)s,%(location)s,%(user_id)s, %(city_id)s)"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_camping(cls, data):
        query = "UPDATE campings SET description=%(description)s, location = %(location)s  WHERE id = %(camping_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_camping(cls, data):
        query = "DELETE FROM campings WHERE id = %(camping_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_camping_by_id(cls, data):
        query = "SELECT * FROM campings LEFT JOIN users on campings.user_id = users.id WHERE campings.id = %(camping_id)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @classmethod
    def delete_users_camping(cls, data):
        query = "DELETE FROM campings WHERE campings.user_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO likes (user_id, camping_id) VALUES (%(id)s, %(camping_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeLike(cls, data):
        query = "DELETE FROM likes WHERE camping_id = %(campings_id)s AND user_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_users_who_liked(cls, data):
        query = "SELECT user_id from likes where likes.camping_id = %(camping_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        uswersWhoLiked = []
        if results:
            for person in results:
                uswersWhoLiked.append(person["user_id"])
        return uswersWhoLiked

    @classmethod
    def delete_all_likes(cls, data):
        query = "DELETE FROM likes where camping_id = %(camping_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_camping(data):
        is_valid = True
        if len(data["description"]) < 3:
            flash("Description be at least 3 characters!", "description")
            is_valid = False
        if len(data["city"]) < 1:
            flash("City is required!", "city")
            is_valid = False
        if not data["location"]:
            flash("Location is required!", "location")
            is_valid = False
        return is_valid

        # if not data["image"]:
        #     flash("File is required!", "image")
        #     is_valid = False
