from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import config
import telebot, time
bot = telebot.TeleBot(config.token)

htmlBuy = 'https://localbitcoins.net/ru/buy_bitcoins'
htmlSell = 'https://localbitcoins.net/ru/sell_bitcoins'

def get_html(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	return(webpage)

def parse(webpage):
	soup = BeautifulSoup(webpage, 'html.parser')
	table = soup.find('table', class_='table table-striped table-condensed table-bitcoins ')
	
	projects = []
	raw_deals = []
	
	for row in table.find_all('tr')[1:]:
		cols = row.find_all('td')
		#print(cols)
		projects.append({
			'User': cols[0].a.text,
			'Bank': cols[1].text.replace('\n', '').replace('                     ', ' ').replace('                ', ' ').replace('                    ', ' '),
			'Price': cols[2].text.split()[0],
			'Limits': cols[3].text.split()[0:3]		})
	
	for i in projects:
			if i not in raw_deals:
				raw_deals.append(i)
				
	return(raw_deals)	

def sort_buy(raw_deals):	
	
	deals = []		
	for d in raw_deals:
		if 'Сбер' in d['Bank'] or 'СБЕР' in d['Bank'] or 'сбер' in d['Bank'] or 'Тин' in d['Bank'] or 'ТИН' in d['Bank'] or 'тин' in d['Bank'] or 'Tin' in d['Bank'] or 'tin' in d['Bank'] or 'SBE' in d['Bank'] or 'Sbe' in d['Bank']:
			if not 'Olegtyun' in d['User']:
				deals.append(d)
	return(deals)




def solve():
	buy = sort_buy(parse(get_html(htmlBuy)))
	sell = parse(get_html(htmlSell))
	SUMM = 107900.0
	NET_PROFIT = -5000
	
	sell_price = (float(sell[0]['Price'])+float(sell[1]['Price']))/2
	
	for b in buy:
		real_summ = min(SUMM, float(b['Limits'][2]))
		profit = sell_price/float(b['Price'])/1.016*real_summ-real_summ
		if profit > NET_PROFIT:
			bot.send_message(90020180, "Хорошая сделка")
			bot.send_message(90020180, ''.join(str(b)))
			bot.send_message(90020180, "Прибыль ")
			bot.send_message(90020180, profit)
			bot.send_message(90020180, "Доступные продавцы")
			bot.send_message(90020180, ''.join(str(sell[0:3])))
			bot.send_message(90020180, htmlBuy)
			
	print(sell[0:3])
	main()
	
				
#@bot.message_handler(commands=['ok'])
#def sleep(message): 
	#time.sleep(20)
	#bot.stop_polling()
	#main()
	
#@bot.message_handler(commands=['start', 'help'])
#def send_welcome(message):
	#bot.reply_to(message, "Howdy, how are you doing?")
	#bot.stop_polling()
	#main()
	
def main():
	#bot.polling()
	try:
		solve()
	except BaseException:
		time.sleep(30)
		main()
	if __name__ == '__main__':
				#bot.polling(none_stop=False, interval = 1, timeout = 10)
				#bot.stop_polling()
				main()

	
main()
#bot.polling()
