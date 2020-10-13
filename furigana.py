import cv2
import io
import pytesseract
import pykakasi
import regex
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

img = cv2.imread('jap.png')

#=======================================
# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def removeBlanks(kanaSet):
	kanaSet[:] = (value for value in kanaSet if value != '') #removes blanks from the list
	return kanaSet

def separateWords(kanaSet, str):
    for kana in kanaSet:
    	if kana in str:
    		str= str.replace(kana,kana+" ")   #adds space after specific kana in set
    return str

def insertFurigana(kanjiSet, furigana, str):
    for i in range(0,len(kanjiSet)):
        if kanjiSet[i] in str:
            str= str.replace(kanjiSet[i],furigana[i])   #adds space after specific kana in set
    return str
#=======================================
img = get_grayscale(img)

file1 = io.open("nihongo.txt","w+",encoding="utf-16")
# s = (pytesseract.image_to_string(img, 'jpn'))
s = "運命だとか未来とかって言葉がどれだけ手を伸ばそうと届かない場所で僕ら恋をする時計の針も二人を横目に見ながら進むそんな世界を二人で一生いや、何章でも"
s = s.replace("\n","")#removes new line
s = s.replace(" ", "") #removes whitespaces

file1.write(s+"\n\n")

print(s)
print("===============================\n")
hir = regex.findall(r'\p{Hiragana}*', s) #gets a list of all the Hiragana
hir = removeBlanks(hir)
print(hir)
print("===============================\n")
kat = regex.findall(r'\p{Katakana}*ー?\p{Katakana}?', s) #gets a list of all the Katakana
kat = removeBlanks(kat)
print(kat)
print("===============================\n")
kanj = regex.findall(r'\p{Han}*', s) #gets a list of all the Kanji
kanj = removeBlanks(kanj)
print(kanj)
print("===============================\n")

furi = []
lis = []
for item in kanj:                           #gets the kana reading of the kanji
    result = pykakasi.kakasi().convert(item)
    furi.append(result[0].get("hira"))
    lis.append(result[0].get("orig")+"("+result[0].get("hira")+") ")

str1=""
for ele in lis:
        str1 += (ele+"\n")

for i in range (0,len(lis)):
    print(kanj[i] +" - "+furi[i])
    print(lis[i]+"\n")

s = separateWords(hir,s)
s = separateWords(kat,s)
s = s.replace(" ,", ", ")
s = insertFurigana(kanj, lis, s)

file1.write(s+"\n\n")
file1.write(str1)

file1.close()

# print(s)
