from karmapash import KarmaPash

kp = KarmaPash()

result = kp.chat("Explain how binary search works.")

print("BLOCKED:", result["blocked"])
print("RESPONSE:", result["response"])
print("DECISION:", result["security"]["policy"]["decision"])