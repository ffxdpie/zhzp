import sys , time ,requests ,re
from notify import send 

#程序的主体部分
def qbc(workp) :

        #获取用户名和token

        url_user= "http://zhzp.qhhcdz.com:9099/loginAuthenticate"
        headers_user = {"User-Agent":"okhttp/3.9.0",
                "Accept":"application/json",
                "Charset":"UTF-8",
                "app":"1",
                "Content-Type":"application/x-www-form-urlencoded",
                "Content-Length":"48",
                "Host":"zhzp.qhhcdz.com:9099",
                "Accept-Encoding":"gzip",
                "User-Agent":"okhttp/3.9.0",
                "Connection":"keep-alive",
                }
        data_user = {"username" : workp,
                "password" : "Gjzhypt816099@"}
        res = requests.post(url=url_user,data=data_user,headers=headers_user)     


        ex1 = '"realname":"(.*?)"'                      #找用户名正则
        User_Info = re.findall(ex1, res.text,re.S)         
        # print("现在登录的用户是"+User_Info[0])          #用户名字
        ex2 ="'Token': '(.*?)'"                          #找Token正则
        User_token = re.findall(ex2 , str(res.headers),re.S)
        if not User_Info  :                                      #判断状态码
                return print("请检查工作证和网络状态")
               
        else:

                #print (User_Info[0]+"的token是"+User_token[0]) 
                print("用户："+User_Info[0])
                token = User_token[0]                  #token
        time.sleep (1)      
        count = 0
        while  count < 3 :
                count =count + 1
                #进入班前一题
                url_bqyt= "http://zhzp.qhhcdz.com:9093/user/exam/getDailyExam?type=4"
                bqythe ={
                        "Accept":"application/json",
                        "Content-type":	"application/x-java-serialized-object",
                        "Charset":"UTF-8",
                        "app":"1",
                        "Content-Type":	"application/json",
                        "Token":"Bearer "+token,
                        "Host":"zhzp.qhhcdz.com:9093",
                        "Accept-Encoding":"gzip",
                        "User-Agent":"okhttp/3.9.0",
                        "Connection":"keep-alive"}
                bq = requests.get(url=url_bqyt,headers=bqythe) 
                bq_number = re.findall('},"status":(.*?)}',bq.text,re.S)
                #print(bq_number[0]) #答题数的状态码
                #print(bq.text)

                if bq_number[0] == '200':                      #判断是否超过最大答题数
                        #print(bq.text)
                        ex3 ='"id":(.*?),"'
                        examUserId = re.findall(ex3 ,bq.text,re.S)
                        #print(examUserId[0])
                        #获取题目
                        dati_url = "http://zhzp.qhhcdz.com:9093/user/exam/getDailyExamQuestions?id="+examUserId[0]
                        dati = requests.get(url=dati_url,headers=bqythe)
                        dati.close()
                        # print(dati.text)                               #打印题目


                        questionId =re.findall('"questionId":(.*?),"',dati.text,re.S)
                        subject_seek = '"type":4,"title":"(.*?)"'
                        subject = re.findall(subject_seek,dati.text,re.S)                  #获取题目
                        examRecordId_seek = '"examRecordId":(.*?),'
                        examRecordId = re.findall(examRecordId_seek,dati.text,re.S)        #这个是examRecordId,提交的时候用
                        answer_id_seek = '"id":(.*?),'                                     #题目的id
                        answer_id = re.findall(answer_id_seek,dati.text,re.S)
                        user_id_seek = '"userId":(.*?),'
                        user_id = re.findall(user_id_seek,dati.text,re.S)                 # user_id

                        #print(answer_id[2])
                        # print("提交答案id"+examRecordId[0])
                        #找答案
                        with open ('siji.txt',encoding="utf-8") as file :
                                content= file.read()
                                #print(content)
                        answer = []
                        for i in (0,1,2):
                                time.sleep (0.5)
                                # print(questionId[i])
                                print(subject[i])
                                #print(answer_id[i])                                    #对每一道题保存答案
                                #用题目检索答案
                                f = subject[i]
                                k = f.replace("(","[(]").replace(")","[)]")   #给这个bi（）加[],为了让他能匹配道题目，fack！！
                                fk = k+'.*?(A|B|C)'
                                daan = re.findall(fk,content)
                                if not daan :
                                        daan.append('B') 
                                answer.append(daan[0])
                                print('本题答案'+answer[i])
                        #print(examRecordId[0])
                        #print(answer_id[3])
                        #print(user_id[0])
                
                        #answer.reverse()
                        #print(answer)
                        for j in (0,1,2):
                            
                                url_answer = "http://zhzp.qhhcdz.com:9093/user/exam/submitExamAnswer"
                                data_answer = {"answer":answer[j],    
                                                "id":answer_id[j]}
                                head_answer = {
                                        "Accept":"application/json",
                                        "Charset":"UTF-8",
                                        "app":"1",
                                        "Token":"Bearer "+token,
                                        "Content-Type":	"application/x-www-form-urlencoded",
                                        "Content-Length":"19",
                                        "Host":"zhzp.qhhcdz.com:9093",
                                        "Accept-Encoding":"gzip",
                                        "User-Agent":"okhttp/3.9.0",
                                        "Connection":"keep-alive"}
                                anwer_chat = requests.post(url=url_answer,data=data_answer,headers=head_answer)
                        # print(anwer_chat.text)
                        time.sleep (1)

                        #全部交卷
                        url_jj = "http://zhzp.qhhcdz.com:9093/user/exam/submitExamPaper"
                        data_jj = {"str":'{"examUserQuestions":[{"answer":"B","id":'+answer_id[0]+'},{"answer":"B","id":'+answer_id[1]+'},{"answer":"A","id":'+answer_id[2]+'}],"id":'+answer_id[3]+',"seminarId":'+examRecordId[0]+',"userId":'+user_id[0],
                                "id":examRecordId[0]}
                        head_jj = { "Accept":"application/json",
                                "Charset":"UTF-8",
                                "app":"1",
                                "Token":"Bearer "+token,
                                "Content-Type":"application/x-www-form-urlencoded",
                                "Content-Length":"278",
                                "Host":"zhzp.qhhcdz.com:9093",
                                "Accept-Encoding":"gzip",
                                "User-Agent":"okhttp/3.9.0",
                                "Connection":"keep-alive"}
                        jj = requests.post(url=url_jj,data=data_jj,headers=head_jj)
                        jj.close()
                        achievement = re.findall('"result":"您未通过考试 (.*?)"',jj.text)[0]
                        print(f"第{count}套题{achievement}")

                        url_sec = "http://zhzp.qhhcdz.com:9093/user/exam/getResultsDetails?id="+examRecordId[0]
                        head_sec ={"Accept":"application/json",
                                "Content-type":	"application/x-java-serialized-object",
                                "Charset":"UTF-8",
                                "app":"1",
                                "Content-Type":"application/json",
                                "Token":"Bearer "+token,
                                "Host":"zhzp.qhhcdz.com:9093",
                                "Accept-Encoding":"gzip",
                                "User-Agent":"okhttp/3.9.0",
                                "Connection":"keep-alive"}
                        win = requests.get(url=url_sec,headers=head_sec)
                        #print(win.text)
                        win.close()
                else :
                        bq.close()
                        count = 3
                        print("今天的题答完了")




#循环和重复
with open(r"user.txt", "r",encoding='UTF-8') as f :
    for line in f:
        qbc(line)
print("by 焚香 (班前一题3.0):找不到的答案就选B")

send("刷题完成","有时间在改进")
