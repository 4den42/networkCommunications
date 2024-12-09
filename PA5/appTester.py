import requests

baseURL = 'http://127.0.0.1:5000'  #URL
def test_fact(amount):
    headers = {'Amount': str(amount)}
    response = requests.get(f"{baseURL}/fact", headers=headers)  #Fact tester
    print(f"Fact Response({amount}):")
    print(response.json())
    print("\n")

def test_info():
    response = requests.get(f"{baseURL}/info")     #Info tester
    print("Info Response:")
    print(response.json())

if __name__ == "__main__":
    print("Testing Flask App...")
    test_fact(15)  
    test_info()  
