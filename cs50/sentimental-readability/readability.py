from cs50 import get_string
t = get_string("Text: ")
wornum = 1
sennum = 0
letnum = 0
for i in range(len(t)):
    if t[i].isalpha():
        letnum += 1
    elif t[i].isspace():
        wornum += 1
    elif t[i] == '.' or t[i] == '!' or t[i] == '?':
        sennum += 1
l = letnum / wornum * 100
s = sennum / wornum * 100
i = 0.0588 * l - 0.29 * s - 15.8
i = round(i)
if i > 16:
    print("Grade 16+")
elif i < 17 and i > 1:
    print(f"Grade {i}")
else:
    print("Before Grade 1")
