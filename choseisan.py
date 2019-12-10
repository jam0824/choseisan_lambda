import datetime
import re
import urllib.request
import urllib

class Choseisan():
    def get_token(self):
        url = 'https://chouseisan.com/'
        response = urllib.request.urlopen(url)
        for key, value in response.getheaders():
            if "chousei_token" in value:
                str_token = value
                break
        m = re.findall(r'chousei_token=.*?;', str_token)
        token = m[0].replace('chousei_token=', '')
        token = token.replace(';', '')
        return token



    def get_chosei_url(self,token, name, kouho):
        url = 'https://chouseisan.com/schedule/newEvent/create'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {
            'name': name,
            'comment': '',
            'kouho': kouho,
            'chousei_token': token
        }
        params = urllib.parse.urlencode(params)
        req = urllib.request.Request(url, data=params.encode("utf-8"), method="POST", headers=headers)
        response = urllib.request.urlopen(req)
        get_url = response.geturl()
        get_url = get_url.replace('https://chouseisan.com/schedule/newEvent/complete', 'https://chouseisan.com/s')
        return get_url

    def get_date(self, num_date, str_time):
        list_day = ["月","火","水","木","金","土","日"]
        str_dates = ""
        today = datetime.date.today()
        for i in range(num_date):
            target_date = today + datetime.timedelta(days=i+1)
            day = target_date.weekday()
            #土日以外を出力
            if day < 5:
                str_dates += target_date.strftime('%m/%d')
                str_dates += "（" + list_day[day] + "）" + str_time + "\n"
        return str_dates
        
    def get_command(self, command):
        dic_command = {}
        list_command = command.split(",")
        dic_command["name"] = list_command[1]
        dic_command["num"] = int(list_command[2])
        dic_command["time"] = list_command[3]
        return dic_command