import requests #downloads webpage
from bs4 import BeautifulSoup #extract info (parse)
import pandas as pd

#first date:2003-01-01
#last date: 2015-05-13

'''
Scrape the following info from wunderground.com and timeanddate.com
1) Precipitation average
2) Temperature average
3) Moisture average
4) Wind averege
5) Sunset time (hour and min)
6) Sunrise time (hour and min)
'''

if __name__ == "__main__":

	dates, avg_temp, avg_moist, avg_prec, avg_wind, sunrise,  sunset =  ([] for i in range(7))

	print("Starting ... \n")
	for year in range(2003,2016):
		for month in range(1,13):
			# take into account leap years
			if year in (2004,2008,2012):
				days_in_month = {1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
			else:
				days_in_month = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
			days = days_in_month[month]
			try: # get sunset and sunrise. All the info per day for a month is in one site so this is inside month loop
				url_ss = 'http://www.timeanddate.com/sun/usa/san-francisco?month=%s&year=%s' %(month, year)
				res = requests.get(url_ss)
				res.raise_for_status()

				site_content = res.content
				parser = BeautifulSoup(site_content, 'html.parser')
				sunrise_parser = parser.find_all("td",class_="c sep")
				sunset_parser = parser.find_all("td",class_="sep c")
				# get sunrise and sunset for every day of the month
				for i in range(days):
					if (year == 2015 and month > 4 and i > 12):
						break
					else:
						sunrise.append(sunrise_parser[(i*3)].text[0:4])
						sunset.append(sunset_parser[(i*4)].text[0:4])
			except Exception as exc:
						  print(' 2.There was a problem: %s' % (exc))   
			for day in range(1,days+1):
				# don't go past 2015-05-13
				if (year == 2015 and month > 4 and day > 13):
					break
				else:
					date = str(month)+"/"+str(day)+"/"+str(year) # save the date
					dates.append(date)
					url_weather = 'https://www.wunderground.com/history/airport/KSFO/%s/%s/%s/DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=' %(year,month,day)
					try: # get weather info. Iterate avery day and get the info.
						res = requests.get(url_weather)
						res.raise_for_status()
						site_content = res.content
						parser = BeautifulSoup(site_content, 'html.parser')
						means = parser.find_all("span",class_="wx-value")                   
						avg_temp.append(means[0].text)  #mean temp
						avg_moist.append(means[8].text) #mean moisture
						avg_prec.append(means[9].text)  #precipitation
						avg_wind.append(means[13].text) #wind
					except Exception as exc:
						print(' 2.There was a problem: %s' % (exc))
						avg_temp.append('99')
						avg_moist.append('99')
						avg_prec.append('99')
						avg_wind.append('99')
			print(" .... done till ... " + str(date))