import firebase_admin # type: ignore
from firebase_admin import credentials, firestore # type: ignore

print("\U0001F680 Test Firebase startar...")  # Debug-meddelande

# Ladda upp anslutningsnyckeln
cred = credentials.Certificate("C:\\Skola\\agila\\project\\Agile-Demo\\exprey-f5b5f-firebase-adminsdk-fbsvc-e717588d99.json")
firebase_admin.initialize_app(cred)

print("\U0001F504 Importerad firebase_admin!")  # Debug-meddelande

# Anslut till Firestore
db = firestore.client()
print("✅ Firebase är initialiserat!")  # Debug-meddelande


# Skapa en testdokument i databasen
def test_firestore():
    print("\U0001F504 Ansluter till Firestore...")  # Debug-meddelande
    test_ref = db.collection("test").document("demo")
    test_ref.set({"message": "Firebase fungerar!"})
    print("✅ Testdata har sparats i Firestore.")


test_firestore()
print("\U0001F389 Skriptet kördes klart!")  # Debug-meddelande