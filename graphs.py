import matplotlib.pyplot as plt

total = 4092
multi = 792
single = total - multi

allcaps = 1372
nocaps = 240
mix = total - allcaps - nocaps
firstcap = 2388
firstuncap = 92
nonalpha= 378
onlyalpha = total - nonalpha
nonalphachar = ['-', '(', ')', '/', '.', '®', '™', ',', '*', '©', '!', '_', '+', '[', ':', ']', '@', "'", '"', '´']
countnonalpha = [239, 82, 70, 21, 23, 2, 1, 4, 7, 1, 1, 8, 4, 5, 2, 1, 1, 10, 2, 1]
test = countnonalpha

x = ['has non-alphanumeric', 'only alphanumeric']
# plt.bar(nonalphachar,test, label="Data 1")
plt.pie(test,  labels = nonalphachar, autopct='%1.1f%%')
# for index, value in enumerate(test):
#     plt.text(value, index,
#              str(value))
plt.title('Count of different non- alphanumeric characters')
# plt.xlabel('non-alphanumeric characters')
# plt.ylabel('Count of each type')
plt.show()