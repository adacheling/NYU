from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import threading, getopt, sys
from mergeFile import merge

class WeatherSpider(object):
  def __init__(self, driver):
    self.driver = driver
    self.state = 'AL'
    self.station = 'acc'
    self.month = '1'
    self.year = '2018'
  def setLoc(self, state):
    self.state = state
  def setSta(self, station):
    self.station = station
  def setMon(self, month):
    self.month = month
  def setYear(self, year):
    self.year = year
  def __tableExtract(self, table, filename):
    rows = table.find_elements_by_tag_name('tr')
    with open(filename, '+w') as f:
      for row in rows:
        cols = row.find_elements_by_tag_name('td')
        rowStr = ''
        for col in cols:
          rowStr += col.text + ','
          print(col.text, end=' ', flush=True)
        if len(cols) != 0: 
          f.write(rowStr + '\n')
          print()
  def start(self, output):
    # request url
    self.driver.get('http://newa.nrcc.cornell.edu/newaLister/rawdat')
    # select state
    selectState = Select(self.driver.find_element_by_name('stabb'))
    selectState.select_by_value(self.state)
    # select month
    selectMon = Select(self.driver.find_element_by_name('month'))
    selectMon.select_by_value(self.month)
    # select year
    selectYear = Select(self.driver.find_element_by_name('year'))
    selectYear.select_by_value(self.year)
    # wait until options of stations are loaded, then select the station 
    option = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, 'option[value="{}"]'.format(self.station)))
    )
    option.click()
    # get report
    getReport = self.driver.find_element_by_css_selector('input[value="Get report"]')
    getReport.click()
    # get table
    table = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.ID, 'dtable'))
    )
    self.__tableExtract(table, output)
    self.driver.close()

def runSpider(state, location, mon, year, output):
  driver = webdriver.PhantomJS()
  spider = WeatherSpider(driver)
  spider.setLoc(state)
  spider.setSta(location)
  spider.setMon(mon)
  spider.setYear(year)
  spider.start(output)

def createThread(target, args):
  return threading.Thread(target=target, args=args)
  
if __name__ == '__main__':
  # options = webdriver.ChromeOptions()
  # options.add_argument('headless')
  # driver = webdriver.Chrome(options=options)
  # driver = webdriver.PhantomJS()
  state = ''
  station = ''
  mon = []
  year = ''
  # argument parser
  argv = sys.argv[1:]
  opts, args = getopt.getopt(argv, 's:w:y:m:')
  for opt, arg in opts:
    if opt == '-s':
      state = arg
    elif opt == '-w':
      station = arg
    elif opt == '-y':
      year = arg
    elif opt == '-m':
      mon = arg.split('-')
  threads = []
  fileList = []
  lo = int(mon[0])
  hi = lo if len(mon) == 1 else int(mon[1])
  # start a thread for each month
  for mon in range(lo, hi + 1):
    t = createThread(runSpider, (state, station, str(mon), year, 'output-'+ str(mon)))
    threads.append(t)
    fileList.append('output-' + str(mon))
    t.start()
  # wait until all the threads are terminated
  for thread in threads:
    thread.join()
  

  output = args[0]
  fileList.reverse()
  merge(fileList, output)





