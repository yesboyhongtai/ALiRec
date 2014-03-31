# encoding=gb2312  
# The data statistics of train dataset
# author by hongtai
# 2014/3/28

import string
def format_train(trainFile, format_train_file):
        lineNum = 1
        print "-----reading train file------"
  
        lineList = [line for line in file(trainFile)]
        out = open(format_train_file, 'w+')
        split_file = []
        for i in range(4,9):
                split_file.append(open(format_train_file+"_"+str(i), 'w+'))
        for line in lineList:
                if lineNum == 1:	#ignore the title in first line
                        lineNum += 1
                        continue

                lineNum += 1
                row = line.split(',') 
                date = row[3]
                date = unicode(date, "gb2312")
                #date.decode('cp936')
                date = date.replace(u'月',' ')
                date = date.replace(u'日',' ')
                #print(date)
                time = date.split(' ')

                #print(date)
                month = time[0]
                #print(month)
                day = time[1]
                row.pop()
                row.append(month)
                row.append(day)

                sep = ','
                new_line = sep.join(row)
                #new_line.join(row, sep)

                out.write('%s\n' % (new_line))
                split_file[string.atoi(month)-4].write('%s\n' % (new_line))
                
def stat_month(format_train_file):
        min = 0
        max = 12
        month_set = []
        lineList = [line for line in file(format_train_file)]
        for line in lineList:
                row = line.split(',')
                month_set.append(row[3])

        ms = set(month_set)
        print(ms)
        return ms
def stat_user(format_train_file):
    user_set = []
    lineList = [line for line in file(format_train_file)]
    for line in lineList:
        row = line.split(',')
        user_set.append(row[0])
    us = set(user_set)
    print(len(us))
def stat_train(trainFile, format_train_file):
        format_train(trainFile, format_train_file)
        stat_month(format_train_file)


def main():
        #format_train("t_alibaba_data.csv", "format_data.csv")
        stat_month("format_data.csv")
        stat_user("format_data.csv")
if __name__ == "__main__":
    main()
    
