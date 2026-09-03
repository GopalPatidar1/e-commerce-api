from app.repository import user
def getUserProfileById(db, id):
   return user.getUserById(db, id)