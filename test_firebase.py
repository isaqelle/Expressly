import os
print("Current working directory:", os.getcwd())
import firebase_admin # type: ignore
from firebase_admin import credentials, firestore # type: ignore

print("\U0001F680 Test Firebase startar...") 

# Ladda upp anslutningsnyckeln
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

print("\U0001F504 Importerad firebase_admin!")  

# Anslut till Firestore
db = firestore.client()
print("✅ Firebase är initialiserat!")  


def test_firestore():
    print("\U0001F504 Ansluter till Firestore...")  
    test_ref = db.collection("test").document("demo")
    test_ref.set({"message": "Firebase fungerar!"})
    print("✅ Testdata har sparats i Firestore.")


test_firestore()
print("\U0001F389 Skriptet kördes klart!") 