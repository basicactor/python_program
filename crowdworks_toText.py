# coding: utf-8
import requests 
import bs4 as bs 
import csv
import pandas as pd
import re
import numpy as np
import subprocess
import time



def get_good_work():
    t1 = time.time()
    title = []
    href =[]
    amount = []

    for i in range(16):
        url = "https://crowdworks.jp/public/jobs/category/37/type/task" +"?page=" + str(i)
        contents = requests. get(url).content
        soup = bs.BeautifulSoup(contents, "html.parser")
    
    

        for i in soup.find_all("h3", class_= "item_title"):
            removed_chr = i.text.replace("文","").replace(",","")
            title.append(removed_chr)   #2,000のような点の区切りを取り除く
            href.append(i.a.get("href"))
            

        for k in soup.find_all("b", class_="amount"):
            text = k.text.replace(",","")
            s = re.search("\S\d*", text)
            amount.append(int(s.group()))
        

        
    df = pd.DataFrame({"title": title,
                        "href":href,
                        "pay":amount},
                        columns = ["title", "pay", "href"])


    find =[]
    for m in df["title"]:
        if re.search("\d*字", m):   
            p = re.search("\d*字", m)
            find.append(p.group())                 
        else:
            find.append("0")
   



    find2 =[]        
    for i in find:
        if not i == "字":
            p2 = re.search("\d*", i)
            find2.append(int(p2.group()))
        else:
            find2.append(0) 

    df["chr_count"] = find2

    new_chr_count =[]      
    for count, href in zip(df["chr_count"],df["href"]):
        if count == 0:
            url =  "https://crowdworks.jp/" + href 
            #url = "https://crowdworks.jp/public/jobs/1483021"
            contents = requests. get(url).content
            soup = bs.BeautifulSoup(contents, "html.parser")
            #with open("crowdworks_detail_page.txt", "w") as f:
            #    f.write(str(soup))


            if soup.find("th", text = "文字数（１記事あたり）"):
                char_from_detail = soup.find("th", text = "文字数（１記事あたり）").find_next_sibling("td").text
                char_from_detail = str(char_from_detail).replace(",","")
                p3 = re.search("\S\d*", char_from_detail)
                char_from_detail= int(p3.group())
                new_chr_count.append(char_from_detail)
            else:
                new_chr_count.append(0)
                
                
            
        else:
            new_chr_count.append(count)

    df["chr_count"] = new_chr_count

    df["pay"] = df["pay"]*0.8

    pay_char_count = []
    for pay, count in zip(df["pay"], df["chr_count"]):
        if count > 0:
            pay_char_count.append(pay/count)
        else:
            pay_char_count.append(0)

    df["pay/chr_count"] = pay_char_count
    
    

    

    df = df.sort_values(by = "pay/chr_count", ascending=False)





    with open("cw:1000円以上案件.txt","w") as f, open("cw:500円〜999円案件.txt", "w") as k:
        for title, rate, href, pay in zip(df["title"], df['pay/chr_count'], df["href"], df["pay"]):
            if pay >= 1000:
                f.write(title)
                f.write(str(pay)+"円"+ "\n")
                f.write(str(rate)+"円"+ "\n")
                f.write("https://crowdworks.jp" + href +"\n")
                f.write("=======================================")
                f.write("\n"*3)
            elif pay > 500 and pay < 1000:
                k.write(title)
                k.write(str(pay)+"円"+ "\n")
                k.write(str(rate)+"円"+ "\n")
                k.write("https://crowdworks.jp" + href +"\n")
                k.write("=======================================")
                k.write("\n"*3)
                
                '''
                disp_title = title
                disp_href = "https://crowdworks.jp/" + href
                disp_rate = str(rate)+"円"
                os.system("osascript -e 'display notification \"{}\"with title \"{}\" subtitle \"{}\"'".format(disp_href,disp_title, disp_rate))
                time.sleep(4)
                '''
                #osascript -e 'display notification "通知したいメッセージ" with title "任意のタイトル" subtitle "任意のサブタイトル"'
    
    t2 = time.time()
    print("=============================================")
    print(t2 - t1)
    subprocess.call("open ~/Python/crawler/cw:1000円以上案件.txt", shell = True)
    subprocess.call("open ~/Python/crawler/cw:500円〜999円案件.txt", shell = True)
if __name__ == '__main__':
    get_good_work()
    


