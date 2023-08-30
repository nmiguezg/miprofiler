# import datetime
# import json
# import configparser

# class Usuario():
#     """Clase que representa un usuario de la red social."""
#     def __init__(self, id, posts) -> None:
#         self.id = id
#         self.posts = posts
#         self.perfilado = {}
#     def actualizar_usuario(self, collection, edad, genero, algoritmo):
#         collection.update_one(
#         self.perfilado[algoritmo] = {'edad': edad, 'genero': genero}
        

# class Coleccion():
#     """Clase que representa una colección de usuarios,
#       cada uno con un conjunto de posts, a perfilar."""
#     def __init__(self, nombre, usuarios, db, collection) -> None:
#         self.nombre = nombre
#         self.fecha_creacion = datetime.now().timestamp()
#         self.usuarios = usuarios
#         self.collection = db[collection]
#         self.collection.insert_one({
#             "nombre": nombre,
#             "fecha_creacion": self.fecha_creacion,
#             "usuarios": usuarios
#         })

#     def perfilar(self, usuarios_perfilados: json):
#         for usuario in usuarios_perfilados['Users']:
#             self.usuarios[usuario.id].actualizar_usuario(usuario.edad, usuario.genero, usuario.algoritmo)

        