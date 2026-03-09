import httpagentparser
 
#10.15.7 is hardcoded in some useragent strings, specifically Chrome and Safari, maybe others, but only Safari provides more info on what the OS may really be
#this part will have to be updated periodically
def checkMacOSX(os, browser):
  if '10.15.7' in os:
    if 'Chrome' in browser:
      os = os + ';Mac OS X 11.x;Mac OS X 12.x;Mac OS X 13.x;Mac OS X 14.x;Mac OS X 26.x'

    if 'Safari' in browser:
      version = browser.split(' ')[1]

      if '14' in version:
        if '14.1' in version:
          os = os + ';Mac OS X 11.3+'
        else:
          os = os + ';Mac OS X 11.0 - 11.2'

      elif '15' in version:
        if '15.6' in version:
          os = os + ';Mac OS X 12.5+'
        elif '15.5' in version:
          os = os + ';Mac OS X 12.4'
        elif '15.4' in version:
          os = os + ';Mac OS X 12.3'
        elif '15.3' in version: #guess, not documented
          os = os + ';Mac OS X 12.2'
        elif '15.2' in version:
          os = os + ';Mac OS X 12.1'
        else:
          os = os + ';Mac OS X 12.0'

      elif '16' in version:
        if '16.6' in version:
          os = os + ';Mac OS X 11.x;Mac OS X 12.x;Mac OS X 13.x'
        elif '16.5' in version:
          os = os + ';Mac OS X 11.x;Mac OS X 12.x;Mac OS X 13.x'
        elif '16.4' in version:
          os = os + ';Mac OS X 11.x;Mac OS X 12.x;Mac OS X 13.x'
        elif '16.3' in version:
          os = os + ';Mac OS X 11.x;Mac OS X 12.x;Mac OS X 13.x'
        elif '16.2' in version:
          os = os + ';Mac OS X 11.x;Mac OS X 12.x;Mac OS X 13.x'
        elif '16.1' in version:
          os = os + ';Mac OS X 11.x;Mac OS X 12.x;Mac OS X 13.x'
        else:
          os = os + ';Mac OS X 11.x;Mac OS X 12.x'

      elif '17' in version:
        os = os + ';Mac OS X 12.x;Mac OS X 13.x;Mac OS X 14.x'

      elif '18' in version:
        if '18.6' in version:
          os = os + ';Mac OS X 13.x;Mac OS X 14.x;Mac OS X 15.6'
        elif '18.5' in version:
          os = os + ';Mac OS X 13.x;Mac OS X 14.x;Mac OS X 15.5'
        elif '18.4' in version:
          os = os + ';Mac OS X 13.x;Mac OS X 14.x;Mac OS X 15.4'
        elif '18.3' in version:
          os = os + ';Mac OS X 13.x;Mac OS X 14.x;Mac OS X 15.3'
        elif '18.2' in version:
          os = os + ';Mac OS X 13.x;Mac OS X 14.x;Mac OS X 15.2'
        elif '18.1' in version:
          os = os + ';Mac OS X 13.x;Mac OS X 14.x;Mac OS X 15.1'
        elif '18.0.1' in version:
          os = os + ';Mac OS X 13.x;Mac OS X 14.x;Mac OS X 15.0.1'
        else:
          os = os + ';Mac OS X 13.x;Mac OS X 14.x;Mac OS X 15'

      elif '26' in version:
        if '26.3' in version:
          os = os + ';Mac OS X 14.x;Mac OS X 15.x;Mac OS X 26.3'
        elif '26.2' in version:
          os = os + ';Mac OS X 14.x;Mac OS X 15.x;Mac OS X 26.2'
        elif '26.1' in version:
          os = os + ';Mac OS X 14.x;Mac OS X 15.x;Mac OS X 26.1'
        else:
          os = os + ';Mac OS X 14.x;Mac OS X 15.x;Mac OS X 26'

  return os



def process(line):
  os,browser,model = httpagentparser.simple_detect(line)
  os = checkMacOSX(os, browser)
  try:
    print('"' + line + '"|"' + os + '"|"' + browser + '"|"' + model + '"')
  except:
    print(line)



def processfile():
  filepath = 'useragent.txt'
  try:
    with open(filepath, "r") as file:
      for line in file:
        if len(line.strip()) > 5:
          process(line.strip())
  except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
  except Exception as e:
    print(f"An error occurred: {e}")



processfile()
