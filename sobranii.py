from bs4 import BeautifulStoneSoup
import re
import zipfile
import os
import shutil

#v1
# Парсится logs.xml и раскидывает по папкам с ошибками

with open("logs.xml", "r", encoding="utf-8") as file:
    xml = file.read()
soup = BeautifulStoneSoup(xml)

def wr(code):
    obj = soup.findAll('httpSample', rc=code)
    print(len(obj))
    os.mkdir(code)
    for num in range(0,len(obj)):
        reqH = obj[num].find('requestHeader').text.strip()
        reqD = obj[num].find('queryString').text.strip()
        resH = obj[num].find('responseHeader').text.strip()
        resD = obj[num].find('responseData').text.strip()
        method = obj[num].find('method').text.strip()

        print(str(num)+'______')
        print(reqH)
        try:
            rez1 = re.split(r'x-Introspect-RqUID: ', reqH)
            rq = re.split(r'authorization', rez1[1])
            name = './' + code + '/'+rq[0].strip()+'.txt'
        except:
            try:
                rez1 = re.split(r'test: ', reqH)
                rq = re.split(r'authorization', rez1[1])
                name = './' + code + '/'+rq[0].strip()+'.txt'
            except:
                try:
                    rez1 = re.split(r'5: ', reqH)
                    rq = re.split(r'authorization', rez1[1])
                    name = './' + code + '/'+rq[0].strip()+'.txt'
                except:
                    try:
                        rez1 = re.split(r'x-introspect-rquid: ', reqH)
                        rq = re.split(r'authorization', rez1[1])
                        name = './' + code + '/'+rq[0].strip()+'.txt'
                        # name = './' + code + '/rquid-low.txt'
                    except:
                        name = './' + code + '/RqUIDpustoi.txt'

# возможно стоит > 80 постввить для rquid = 60

        if len(name) > 70:
            name = name[:38] + '.txt'

        with open(name, "a", encoding='utf-8') as file:
            file.write('Code: '+code + '\n'+'Method: ' +method +'\n'+ '\n'+reqH+'\n'+reqD+'\n'+ resH +'\n'+resD)


wr('200')
wr('400')
wr('401')
wr('405')

#Проверка 200 ответа для правильных значений и повторного токена

os.chdir('./200/')
ind = []
def chek(file1):
    code1 = 'accept: application/json\ncontent-type: application/json'
    code2 = 'x-ibm-client-id: 532f67a0-a57b-40d2-8de9-e18b829e0a0f'
    code3 = '"HPAN": "783dec0778cd041fd4459d3bcb580445002980dd",\n\n  "BIN": "12345678",\n\n  "Amount": "40.09",\n\n  "Currency": "RUB",\n\n  "MCC": "9999",\n\n  "Email": "ecom5665@mail.ru" '
    code4 = 'authorization: Bearer '

    f = open(file1, "r")
    str1 = f.read()
    exist1 = code1 in str1
    print(exist1)

    exist2 = code2 in str1
    print(exist2)

    exist3 = code3 in str1
    print(exist3)
    exist4 = code4 in str1
    print(exist4)
    str2 = str1[178:215]
    f.close()
    if str2 in ind:
        try:
            os.mkdir('негативный сценарий')
        except:
            pass
        with zipfile.ZipFile('./негативный сценарий/использованный токен.zip', 'a') as myzip:
                myzip.write(file1)


    else:
        ind.append(str2)
        if (exist1+exist2+exist3+exist4)==4:
            print(os.getcwd())
            print(file1)
            print("Совпадает")
            try:   
                os.mkdir('позитивный сценарий')
            except:
                pass
            with zipfile.ZipFile('./позитивный сценарий/позитивный сценарий.zip', 'a') as myzip:
                    myzip.write(file1)


files = os.listdir()
files = filter(lambda x: x.endswith('.txt'), files) 
for file1 in files:
    chek(file1)

print(os.getcwd())

#Проверка и определение неправильных параметров с помощью сравнения с каждым файлом(для всех видов ошибок) chek - 200, check1 - 400,401,405

znach = {'method':'Method: POST',
    'accept':'accept: application/json', 
    'content-type':'content-type: application/json',
    'x-Introspect-RqUID':'x-Introspect-RqUID: ',
    'authorization':'authorization: Bearer',
    'x-ibm-client-id':'x-ibm-client-id: 532f67a0-a57b-40d2-8de9-e18b829e0a0f',
    'HPAN':'"HPAN": "783dec0778cd041fd4459d3bcb580445002980dd"',
    'BIN':'"BIN": "12345678"',
    'Amount':'"Amount": "40.09"',
    'Currency':'"Currency": "RUB"',
    'MCC':'"MCC": "9999"',
    'Email':'"Email": "ecom5665@mail.ru"'}
def chek(file1):
    for key in znach:
        f = open(file1, "r")
        str1 = f.read()
        exist = znach[key] in str1
        f.close()
        if exist==0:
            print(key)
            print(file1)
            print('______')
            try:
                os.mkdir('негативный сценарий')
            except:
                pass
            
            with zipfile.ZipFile('./негативный сценарий/изменен параметр '+key+'.zip', 'a') as myzip:
                myzip.write(file1)
def chek1(file1):
        for key in znach:
            try:
                f = open(file1, "r")
                str1 = f.read()
                str1 = str1[:600]
                exist = znach[key] in str1
                f.close()
                if exist==0:
                    print(key)
                    print(file1)
                    print('______')
                    if (os.getcwd()=='C:\\Users\\User\\Desktop\\prog\\python\\парсилки\\400') and (key=='method'):
                        try:
                            os.mkdir('негативный сценарий')
                        except:
                            pass
                        with zipfile.ZipFile('./негативный сценарий/изменен параметр '+key+'.zip', 'a') as myzip:
                            myzip.write(file1)
                        os.remove(file1)
                    
                    else:

                        try:
                            os.mkdir('позитивный сценарий')
                        except:
                            pass
                        
                        with zipfile.ZipFile('./позитивный сценарий/изменен параметр '+key+'.zip', 'a') as myzip:
                            myzip.write(file1)
                        os.remove(file1)
            except:
                pass





files = os.listdir()
files = filter(lambda x: x.endswith('.txt'), files)


for file1 in files:
    chek(file1)


print(os.getcwd())
os.chdir('..')


os.chdir('./400/')
files = os.listdir()
files = filter(lambda x: x.endswith('.txt'), files)


for file1 in files:
    chek1(file1)

#скидывает оставшиеся файлы в архив с измененным rquid

print(os.getcwd())
files = os.listdir()
files = filter(lambda x: x.endswith('.txt'), files)
for file1 in files:
    with zipfile.ZipFile('./позитивный сценарий/изменен параметр x-Introspect-RqUID.zip', 'a') as myzip:
        myzip.write(file1)
    os.remove(file1)


os.chdir('..')
os.chdir('./401/')

files = os.listdir()
files = filter(lambda x: x.endswith('.txt'), files)


for file1 in files:
    chek1(file1)


#скидывает оставшиеся файлы в архив с измененным authorization

print(os.getcwd())
files = os.listdir()
files = filter(lambda x: x.endswith('.txt'), files)
for file1 in files:
    with zipfile.ZipFile('./позитивный сценарий/изменен параметр authorization.zip', 'a') as myzip:
        myzip.write(file1)
    os.remove(file1)



os.chdir('..')
os.chdir('./405/')

files = os.listdir()
files = filter(lambda x: x.endswith('.txt'), files)


for file1 in files:
    chek1(file1)


print(os.getcwd())

# записываем конечные zip архивы и удаляем папки

os.chdir('..')
def write_zip(osh):
    z = zipfile.ZipFile(osh+'_test.zip', 'w')
    try:
        for root, dirs, files in os.walk('./'+osh+'/негативный сценарий'):
            for file1 in files:
                z.write(os.path.join(root,file1))
                print(root,file1)
    except:
        pass

    try:
        for root, dirs, files in os.walk('./'+osh+'/позитивный сценарий'):
            for file1 in files:
                z.write(os.path.join(root,file1))
                print(root,file1)
    except:
        pass
    z.close()

write_zip('200')
write_zip('400')
write_zip('401')
write_zip('405')



shutil.rmtree('./200')
shutil.rmtree('./400')
shutil.rmtree('./401')
shutil.rmtree('./405')
