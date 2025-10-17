from datetime import datetime, timedelta
from typing import List, Dict

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = "https://www.ukr.net/news/main.html"
LOCAL_HTML = "ukr_net_page.html"
NEWS_CSV = "news.csv"
NEWS_DAYS = 5
DATA_FORMAT = "%d-%m-%Y"


def fetch_full_html(url: str, output_file: str) -> None:
	"""
	The function loads a full HTML page with dynamic content using Playwright,
	scrolls it to the end to load all elements, and saves the result to a file.
	It opens the page in a headless Chromium browser, simulates	scrolling down
	to the end, waits for the content to load, and then saves the full HTML
	to a local file.
	Parameters:
		- url : str The URL of the page to load.
		- output_file : str, optional The name of the file to which the HTML code
		- of the page will be saved (defaults to "full_page.html").
	Returns: None
	Exceptions:
		Displays an error message if the page failed to load or if there was
		another problem while the browser was running.
	"""
	try:
		with sync_playwright() as p:
			browser = p.chromium.launch(headless=True)
			page = browser.new_page()
			page.goto(url, timeout=8000)
			
			previous_height = 0
			while True:
				page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
				page.wait_for_timeout(1000)
				current_height = page.evaluate("document.body.scrollHeight")
				if current_height == previous_height:
					break
				previous_height = current_height
			
			html = page.content()
			with open(output_file, "w", encoding="utf-8") as f:
				f.write(html)
			
			browser.close()
		print(f"Full HTML file of '{url}' saved to '{output_file}' file")
	except Exception as e:
		print(f"ERROR: Failed to load '{url}' page.: {e}")
	return


def parse_news(soup: BeautifulSoup) -> List[Dict[str, str]]:
	"""
	The function parses the HTML structure of the news page and extracts
	a list of news items as dictionaries. It goes through all news items
	(section.im), extracts the title, link, raw publication time (raw_time)
	and short description (summary) with the source og news. All news items
	are returned as a list of dictionaries with the keys: title, link, raw_time,
	summary.
	Parameters:
		soup : BeautifulSoup A BeautifulSoup object containing the HTML code
		of the 'ukr.net' page.
	Returns: List[Dict[str, str]] A list of news items, where each news item
	is represented by a dictionary with the keys:
		- "title": the news item title
		- "link": the URL to the full news item
		- "raw_time": the raw text of the publication time (for example, "14:32"
		or "10 Oct")
		- "summary": source of the news item
	Exceptions:
		If the structure of a separate news item is damaged or the element
		is not found, the news item is skipped and a warning is displayed
		in the console.
	"""
	news_list: List[Dict[str, str]] = []
	articles = soup.select("section.im")
	
	for article in articles:
		try:
			title_tag = article.select_one("a.im-tl_a")
			title = title_tag.get_text(strip=True)
			link = title_tag["href"]
			
			time_tag = article.select_one("time.im-tm")
			raw_time = time_tag.get_text(strip=True).replace("\xa0",
			                                                 " ") if time_tag else ""
			
			source_tag = article.select_one("div.im-pr")
			summary = source_tag.get_text(strip=True) if source_tag else ""
			
			news_list.append({"title": title, "link": link,
			                  "raw_time": raw_time, "summary": summary
			                  })
		
		except Exception as e:
			print(f"Error: Failed to process news item: {e}")
			continue
	
	return news_list


def resolve_dates(news_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
	"""
	The function processes the 'raw_time' field in each news item and adds
	a normalized publication date. It analyzes the raw time ('raw_time')
	of the news item, which can be in the format "HH:MM" or "DD MMM",
	and determines the exact publication date. It takes into account that
	the news items on the page can be sorted in reverse chronological order, so
	when switching to a later time, it adjusts the current date back by one day.
	After processing, it adds the 'date' field in format - DD-MM-YYYY
	and removes 'raw_time'.
	Parameters:
		- news_list : List[Dict[str, str]] A list of news items, where each news
		item contains the key 'raw_time' with the raw publication time.
	Returns:
		List[Dict[str, str]] A list of news items with the key 'date'
		(in the format DD-MM-YYYY) added instead of 'raw_time'.
	"""
	ukr_months = {
		'січ': 1, 'лют': 2, 'бер': 3, 'квіт': 4, 'тра': 5, 'чер': 6,
		'лип': 7, 'сер': 8, 'вер': 9, 'жов': 10, 'лис': 11, 'гру': 12
	}
	
	current_date = datetime.now().date()
	previous_minutes = 24 * 60
	resolved: List[Dict[str, str]] = []
	
	for item in news_list:
		raw_time = item.get("raw_time", "")
		date = ""
		
		if ":" in raw_time:
			hour, minute = map(int, raw_time.split(":"))
			current_minutes = hour * 60 + minute
			if current_minutes > previous_minutes:
				current_date -= timedelta(days=1)
			previous_minutes = current_minutes
			date = current_date.strftime(DATA_FORMAT)
		elif raw_time:
			parts = raw_time.split()
			if len(parts) == 2:
				day_str, month_str = parts
				day = int(day_str)
				month = ukr_months.get(month_str.lower()[:3])
				if month:
					year = current_date.year
					if month > current_date.month:
						year -= 1
					current_date = datetime(year, month, day).date()
					previous_minutes = 24 * 60
					date = current_date.strftime(DATA_FORMAT)
		else:
			date = current_date.strftime(DATA_FORMAT)
		
		item["date"] = date
		del item["raw_time"]
		resolved.append(item)
	
	return resolved


def filter_recent_news(data: List[Dict[str, str]], days: int) -> List[
	Dict[str, str]]:
	"""
	The function filters the list of news items, leaving only those that were
	published within the last 'days' days. It compares the date of each news item
	with the current date and cuts off those that are older than the specified
	threshold. The date format in the news items must match the DATA_FORMAT
	pattern (for example, "%d-%m-%Y").
	Parameters:
		- data : List[Dict[str, str]] A list of news items, where each news item
		contains the key "date" in string format.
		- days : int The number of days that are considered "fresh"
		(for example, 3 is news items for the last 3 days inclusive).
	Returns:
		filtered_news: List[Dict[str, str]] A list of news items that were
		published within the last N days.
	"""
	today = datetime.now().date()
	news_period = today - timedelta(days=days)
	
	filtered_news = [item for item in data if
	                 item.get("date") and news_period <= datetime.strptime(
		                 item["date"], DATA_FORMAT).date() <= today]
	
	return filtered_news


def save_to_csv(data: List[Dict[str, str]], filename: str) -> pd.DataFrame:
	"""
    The function saves a list of news items to a CSV file and returns
    a DataFrame for further processing.
    Parameters:
    	- data : List[Dict[str, str]] A list of news items, where each news item
    	is represented by a dictionary.
    	- filename : str The name of the file to which the CSV will be saved.
	Returns:
		pd.DataFrame A DataFrame with news items that can be used
		for statistics or analysis.
    """
	try:
		df = pd.DataFrame(data)
		df.to_csv(filename, index=False, encoding="utf-8-sig")
		print(f"The {filename} файл was saved.")
		return df
	except Exception as e:
		print(f"ERROR: Failed to save CSV file: {e}")
		return pd.DataFrame()


def print_news_stats(df: pd.DataFrame) -> None:
	"""
	The function displays the number of news items for each date
	in a table format.
	Parameters:
		- df : pd.DataFrame A news table containing a 'date' column.
	"""
	if "date" not in df.columns or df.empty:
		print("!!! WARNING: No data for statistics !!!")
		return
	
	stats_df = (
		df["date"]
		.value_counts()
		.sort_index()
		.reset_index()
		.rename(columns={"index": "date", "date": "date"})
	)
	
	print("\nNumber of news items by date:")
	print(stats_df.to_string(index=False))


def main():
	"""
	The main function that manages the full cycle of processing news from
	the 'ukr.net' page:
		- Loads the HTML page with news
		- Parses the structure of the news
		- Normalizes publication dates
		- Filters news for the last N days
		- Saves the result to a CSV file and displays statistics
	Uses global constants:
		- URL: address of the news page
		- LOCAL_HTML: path to the local HTML file
		- NEWS_DAYS: number of days to filter news
		- NEWS_CSV: name of the output CSV file
	Exceptions:
		At each stage of processing, try-except blocks are provided to output
		errors without crashing the program.
	"""
	try:
		fetch_full_html(URL, LOCAL_HTML)
	except Exception as e:
		print(f"ERROR: Failed to load page: {e}")
		return
	
	try:
		with open(LOCAL_HTML, "r", encoding="utf-8") as f:
			soup = BeautifulSoup(f.read(), "html.parser")
	except Exception as e:
		print(f"ERROR: Could not read HTML file: {e}")
		return
	
	try:
		raw_news = parse_news(soup)
		resolved_news = resolve_dates(raw_news)
		recent_news = filter_recent_news(resolved_news, days=NEWS_DAYS)
		data_file = save_to_csv(recent_news, NEWS_CSV)
		print_news_stats(data_file)
	except Exception as e:
		print(f"ERROR: Error processing news: {e}")
		return


if __name__ == "__main__":
	main()
