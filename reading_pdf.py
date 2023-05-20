from PyPDF2 import PdfReader
import os
from datetime import datetime

def addCount(name, dictionary):
    if name in dictionary:
        dictionary[name] += 1;
    else:
        dictionary[name] = 1
    return dictionary

def printRank(dictionary):
    list = [key for key in dict(sorted(dictionary.items(), key=lambda x: x[1]))]
    count = len(list)
    count = 500
    for number in range(count):
        word =list.pop();
        print("  * [ " + str(number + 1) + "위 ] \'" + word + "\' (" + str(dictionary[word]) + "회)")

def writeTxt(dictionary, firstLine, files, fileName):
    pdfFiles = [" "]
    for pdf in files:
        pdfFiles.append(pdf + ".pdf")
    list = [key for key in dict(sorted(dictionary.items(), key=lambda x: x[1]))]
    file = open(fileName, 'w')
    file.write(firstLine + "\n\n\n * 통계에 활용된 파일들:" + "\n  -  ".join(pdfFiles) + "\n\n\n\n\n")
    for number in range(len(list)):
        word = list.pop();
        file.write("\n  * [ " + str(number + 1) + "위 ] \'" + word + "\' (" + str(dictionary[word]) + "회)")
    file.close()


w1 = {}
w2 = {}

error = 0

banWords = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    " ", "  ", "   ", ""
]

additionalBanWords = [
    "an", "the", "i", "you", "we", "he", "she", "they", "it", "this", "that", "them", "us",
    "be", "am", "are", "is", "was", "were", "can", "will", "would", "may",
    "do", "have", "has", "make", "comes", "think", "had", "get", "need", "does",
    "my", "your", "their", "his", "her", "mine", "yours", "hers", "its",
    "who", "when", "whom", "where", "what", "which", "how",
    "as", "of", "to", "in", "and", "that", "for", "from", "with", "on", "our", "by", "at", "than", "more", "or", "but", "even", "up",
    "out", "not", "two", "one", "then", "about", "much", "example", "no", "if", "most", "so", "such", "all", "other", "only", "because", "many"
    "people", "time", "new"
]

files = []

while(True):
    givenName = input("  * 추가 할 파일 이름을 입력해주세요 (확장자 제외) : ")
    if givenName == "":
        print("  * 파일을 로딩하고 통계를 내는 데 시간이 오래 소요될 수 있습니다")
        break
    elif not os.path.isfile(givenName + ".pdf"):
        print("  * 파일 이름을 확인해주세요")
    else:
        print("  * 파일이 추가되었습니다: " + givenName +  ".pdf")
        print("  * 또 추가하실 파일의 이름을 입력해주세요 (작업을 중단하시려면 입력 하지 않고 Enter 키를 누르세요)")
        files.append(givenName)

for fileName in files:
    pdf = PdfReader(fileName + ".pdf")
    print("  *** 파일을 불러왔습니다: " + fileName + ".pdf")
    for pageNumber in range(len(pdf.pages) - 1):
        context = pdf.pages[pageNumber].extract_text()
        for word in context.split(' '):
            if not word.encode().isalpha():
                error += 1 #영어가 아님
            else:
                www = word.lower()
                if www in banWords:
                    error += 1 #오류
                elif www in additionalBanWords:
                    w1 = addCount(www, w1)
                else:
                    w2 = addCount(www, w2)
    print("  *** 파일을 닫았습니다: " + fileName + ".pdf")

notFiltered = w2.copy()
notFiltered.update(w1)

current = datetime.now()
date = str(current.year) + str(current.month) + str(current.day)

fileName1 = "필터링을 거친 결과물 (" + date + ").txt"
fileName2 = "필터링을 거치치 않은 결과물 (" + date + ").txt"

if os.path.isfile(fileName1):
    os.remove(fileName1)
    print(" ***** 기존 파일 ( " + fileName1 + " ) 이 제거 되었습니다")

if os.path.isfile(fileName2):
    os.remove(fileName2)
    print(" ***** 기존 파일 ( " + fileName2 + " ) 이 제거 되었습니다")

writeTxt(w2, " * 다음 단어를 제외한 수치 입니다: " + ", ".join(additionalBanWords), files, "필터링을 거친 결과물 (" + date + ").txt")
writeTxt(notFiltered, " * 아무런 필터링을 거치치 않은 수치 입니다", files, "필터링을 거치치 않은 결과물 (" + date + ").txt")

print(" ------- 파일이 저장 되었습니다 -------")
