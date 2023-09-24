class User():
    def __init__(
        self,
        id: str,
        posts: list[str],
        gender: str,
        age: str,
        collection_id: str
    ) -> None:
        self.id = id
        self.posts = posts
        self.gender = gender
        self.age = age
        self.collection = collection_id
