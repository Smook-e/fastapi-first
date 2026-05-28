import jwt

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjcsImV4cCI6MTc3OTc5MDQ0NX0.do6OJd_EkU-jeT3fJ2yDS6PFOp8tr31_MrZw0LjqCmM"
SECRET_KEY = "b72cf886b4309077f4c3cbb537244daa878e53a02520cc287bb95d8270fa08b2"

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    print(payload)
except Exception as e:
    print(type(e).__name__, e)