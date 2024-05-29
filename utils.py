import chromadb
import face_recognition



known_image = face_recognition.load_image_file("IMG_0623.jpg")
biden_embeddings = face_recognition.face_encodings(known_image)[0]
print(len(biden_embeddings))

print(biden_embeddings)
