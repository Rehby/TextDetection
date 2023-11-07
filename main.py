import easyocr
import os
import re
import fnmatch

reader= easyocr.Reader(['en','ru'], gpu = True)
for folder in os.listdir('rescutcolor'):
    for folder1 in os.listdir(f'rescutcolor/{folder}/'):
        for file in fnmatch.filter(os.listdir(f'rescutcolor/{folder}/{folder1}/'), '*.jpg'):
            result=reader.readtext(f'rescutcolor/{folder}/{folder1}/{file}',detail=0,y_ths=0.4, paragraph=True, decoder='wordbeamsearch',canvas_size=4000)
            flag=0
            if not os.path.exists(f'res_innop/{folder}/{folder1}'):
                os.makedirs(f'res_innop/{folder}/{folder1}')
            
            with open(f'res_innop/{folder}/{folder1}/res.txt','a') as f:
                for i,item in enumerate(result):
                    # if re.match(r'([а-яА-Яё0-9a-zA-Z ()\[\]\.,;]*)([?:]+)',item):
                    # if i in (0,1,2):
                    #     f.write(f'{item}\n')
                    # if ("Выберите" in item and 'ответ' in item) or "?" in item:
                    #     f.write(f'\n\nОтветы\n\n\n')
                    #     break
                    
                    if ("Выберите" in item and 'ответ' in item and flag==0) or "?" in item:
                        f.write(f'{item}\n')
                        f.write(f'\nОтветы\n')
                        flag=1

                    elif flag==0 and i==3:
                        f.write(f'\nОтветы\n')
                        f.write(f'{item}\n')
                        flag=1
                    
                    elif "Назад" in item or "Далее" in item:
                        f.write(f'__________________________________________\n\n')
                        break
                    else:
                        f.write(f'{item}\n')
        

        