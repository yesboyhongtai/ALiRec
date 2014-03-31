# sort the training data by user and then brand
# @author: Zhang Hongtai
# @date 2014.3.31

from math import sqrt

def train_sort(trainFile, sortFile):
  records = []
  rankedLine = []
  lineNum = 1
  
  lineList = [line for line in file(trainFile)]
  for line in lineList:
    if lineNum == 1:	#ignore the title in first line
      lineNum += 1
      continue

    records.append(line)
    lineNum += 1
  
  for line in records:   
    (user, brand, action, month, day) = line.split(',')  
    rankedLine.append((int(user), int(brand), action, month, day))

  rankedLine.sort()
  #rankedLine.reverse()
  
  out = file(sortFile, 'w')
  for (user, brand, action, month, day) in rankedLine[0:len(rankedLine)]: 
    out.write('%d %d %s %s %s' % (user, brand, action, month, day))
  
  return rankedLine
def main():
    train_sort("format_data.csv", "train_sort.txt")
                                 
if __name__ == "__main__":
    main()
