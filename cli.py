import requests

BASE = "http://127.0.0.1:5000"

def menu():
    while True:
        print("\n=== INVENTORY CLI ===")
        print("1. View inventory")
        print("2. Lookup product by barcode")
        print("3. Add product (lookup + add)")
        print("4. Update quantity")
        print("5. Delete product")
        print("6. Exit")
        choice = input("Choose: ")

        if choice == '1':
            r = requests.get(f"{BASE}/inventory")
            print(r.json())
        elif choice == '2':
            barcode = input("Enter barcode: ")
            r = requests.get(f"{BASE}/lookup/{barcode}")
            print(r.json())
        elif choice == '3':
            barcode = input("Enter barcode: ")
            lookup = requests.get(f"{BASE}/lookup/{barcode}").json()
            if 'error' in lookup:
                print("Not found in OpenFoodFacts")
                name = input("Enter name manually: ")
                lookup = {"barcode": barcode, "name": name, "brand": "Unknown"}
            qty = int(input("Quantity: "))
            lookup['quantity'] = qty
            r = requests.post(f"{BASE}/inventory", json=lookup)
            print(r.json())
        elif choice == '4':
            barcode = input("Barcode to update: ")
            qty = int(input("New quantity: "))
            r = requests.put(f"{BASE}/inventory/{barcode}", json={"quantity": qty})
            print(r.json())
        elif choice == '5':
            barcode = input("Barcode to delete: ")
            r = requests.delete(f"{BASE}/inventory/{barcode}")
            print("Deleted" if r.status_code==204 else r.json())
        elif choice == '6':
            break

if __name__ == "__main__":
    menu()