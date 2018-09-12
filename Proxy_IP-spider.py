import urllib.request  
from bs4 import BeautifulSoup
from lxml import etree

url = "http://www.xicidaili.com/nn"  
ip_list=[]
headers = {'Accept': '*/*',
           'Accept-Language': 'en-US,en;q=0.8',
           'Cache-Control': 'max-age=0',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive',
           'Referer': 'http://www.xicidaili.com/nn'
           }


def get_ip_list(url,headers,ip_num):
	i=0
	request = urllib.request.Request(url,None,headers)  
	response = urllib.request.urlopen(request)  
	html = response.read().decode('utf-8') 
	soup = BeautifulSoup(html, "html.parser")

	datas_ip = etree.HTML(html).xpath('//table[contains(@id,"ip_list")]/tr/td[2]/text()')
	datas_port = etree.HTML(html).xpath('//table[contains(@id,"ip_list")]/tr/td[3]/text()')

	while(len(ip_list)<ip_num):
		
		user_agent ='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
		headers_test = {'User-Agent':user_agent}
		proxy = {'http':'http://%s:%s'%(datas_ip[i],datas_port[i])}
		proxy_handler = urllib.request.ProxyHandler(proxy)
		opener = urllib.request.build_opener(proxy_handler)
		urllib.request.install_opener(opener)

		test_url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-09-11&leftTicketDTO.from_station=CDW&leftTicketDTO.to_station=GYW&purpose_codes=ADULT"
		ip_str = str(datas_ip[i]+":"+datas_port[i])
		try:
			req = urllib.request.Request(url=test_url,headers=headers_test)
			res = urllib.request.urlopen(req,None,timeout=10)
			try:
				content = res.read()
				if content:
					print(ip_str +"  可用")
					ip_list.append(ip_str) 
				else:
					print(ip_str +"  不可用")
			except Exception as e:
				continue
		except Exception as e:
			continue
		i+=1

	return ip_list
	   

if __name__ == '__main__':
	num = input("输入爬取IP数量：")
	print(get_ip_list(url,headers,int(num)))



	
		





  
