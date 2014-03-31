# coding=gb2312  
# labels test data by ACTION：msg = 2 > click = 1 > rec = 0  
# test<userA,userB,times,aciton>  - > userBList<2,1,0,0> 
# @author Zhang Hongtai
# @date 2014.3.31
# filter the replicated usrB, revised by cheng yan, 2012-08-21

from math import *

def labelstrain(data):
    labels = []
    lst_user = "="
    BrandAction = {}
    BrandActionList = ""
    Records = []
    userRecRecords = ""
    
    for line in data:
        (user, brand, action, month, day) = line.split(',')
    #action = action[:-1]

    #if userA == "USER_ID_A":
    #  continue

        if lst_user == "=" or user == lst_user:
            key = (int(user), int(brand))
            BrandAction.setdefault(key, -1)
            BrandAction[key] = max(BrandAction[key], getActionScore(action))
        else:
            line = 1
            keys = BrandAction.keys()
            keys.sort()	#dict may be no order, should sort by key
            for key in keys:
                if line == 1:
                    BrandActionList += str(BrandAction[key])
                    userRecRecords += str(key[0]) + " " + str(key[1])
                else:
                    BrandActionList += " " + str(BrandAction[key])
                    userRecRecords += " " + str(key[1])
                line += 1
            
            labels.append(BrandActionList)
            Records.append(userRecRecords)
        
            BrandAction = {}
            BrandActionList = ""
            userRecRecords = ""
            key = (int(user), int(brand))
            BrandAction.setdefault(key, -1)
            BrandAction[key] = max(BrandAction[key], getActionScore(action))
        lst_user = user
    
    
    #for the last group
    line = 1
    keys = BrandAction.keys()
    keys.sort()	#dict may be no order, should sort by key
    for key in keys:
        if line == 1:
            BrandActionList += str(BrandAction[key])
            userRecRecords += str(key[0]) + " " + str(key[1])
        else:
            BrandActionList += " " + str(BrandAction[key])
            userRecRecords += " " + str(key[1])
        line += 1
    labels.append(BrandActionList)
    Records.append(userRecRecords)
    
    return labels, Records

def getActionScore(action):
    if action == "0": #click
        return 0.5
    elif action == "2": #favor
        return 1.5
    elif action == "3": #cart
        return 2
    else: #purchase
        return 2.5

def labels_train(train_sort_File, label_train_file,brand_candidate_file):
    print "-----reading train file ... "
    
    records = [line for line in file(train_sort_File)]
    
    print "-----label train file ... "
    
    print len(records)
    labels, rec_records = labelstrain(records)
    print len(labels)
    
    print "-----output label_train file ... "
    
    out = file(label_train_file, 'w')
    for (brand) in labels[0:len(labels)]:
        out.write('%s\n' % (brand))
        
        
    print "-----output brand recommend file ... "
    
    out = file(brand_candidate_file, 'w')
    for (user_brand_list) in rec_records[0:len(rec_records)]: 
        out.write('%s\n' % (user_brand_list))
        
    print "Ending"


def main():
    labels_train("format_data.csv", "label_train.txt", "brand_candidate.txt")
                                 
if __name__ == "__main__":
    main()
