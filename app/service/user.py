from app.repositories import user
def getUserProfileById(db, id):
   return user.getUserById(db, id)