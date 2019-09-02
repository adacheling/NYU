import os
def merge(fileList, outputFile):
  with open(outputFile, 'w+') as f:
    for file in fileList:
      with open(file) as f1:
        for line in f1:
          f.write(line)
      os.remove(file)

# if __name__ == "__main__":
#   fileList = ['nylga_2016','nylga_2015','nylga_2014']
#   merge(fileList, 'nylga')
    
        