# compute the times of action(click|favor|cart|purchase) for each brand
# compute the favor, cart, purchase as positive vote, the click as false vote, then use "wilson interval"
# @author: hongtai
# @date: 2014-03-31

from math import sqrt

def getActionScore(action):
    if action == "0": #click
        return 0.5
    elif action == "2": #favor
        return 1.5
    elif action == "3": #cart
        return 2
    else: #purchase
        return 2.5

def compute_interaction(data):
    interaction = {}

    for line in data:
        (user,brand,action,month,day) = line.split(',')
        #action = action[:-1]
        key = brand + " " + action
        interaction.setdefault(key, 0)
        interaction[key] += 1

    return interaction

def compute_user_history_interaction(trainFile):
    records = []
    lineList = []
    lineNum = 1
    result = []

    lineList = [line for line in file(trainFile)]
    for line in lineList:
        if lineNum == 1:	#ignore the title in first line
            lineNum += 1
            continue
        records.append(line)
        lineNum += 1

    interaction = compute_interaction(records)
    out = file('user_interaction.txt', 'w')
    for (key, times) in interaction.items():
        out.write('%s %d' % (key, times))
        out.write('\n')

    for (key, times) in interaction.items():
        brand, action = key.split(' ');
        result.append((brand, action, times))


    return result

#get the weight for each type of action
def get_action_weight(action):
    pop = 0;
    if action == "0": #click
        pop = 1
    elif action == "2": #favor
        pop = 1.5
    elif action == "3": #cart
        pop = 2
    else: #purchase
        pop = 3

    return pop;

def compute_confidence(ups, downs):
    n = ups + downs
    if n == 0:
        return 0
    z = 1.0 #1.0 = 85%, 1.6 = 95%
    phat = float(ups) / n

    return (phat+z*z/(2*n)-z*sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n) 

#trainFile line like: [user, brand, action(click|favor|cart|purchase), month, day]
def compute_brand_popularity(trainFile, brand_popularity_file):
    ups = {}
    downs = {}
    popDict = {}
    rankedscores = []
    result = []

    print "-----compute_brand_history_interaction ... "

    interaction = compute_user_history_interaction(trainFile)

    print "-----compute_brand_popularity ... "

    # compute favor, cart, purchase as positive vote(ups), compute click as false vote(downs)
    for (brand, action, times) in interaction[0:len(interaction)]:
        ups.setdefault(brand, 0)
        downs.setdefault(brand, 0)
        ups.setdefault(brand, 0)
        downs.setdefault(brand, 0)
        if action != "0":
            ups[brand] += get_action_weight(action) * times
        else:
            downs[brand] += get_action_weight(action) * times

    # compute confidence interval using wilson interval
    for (brand, votes) in ups.items():
        popDict[brand] = compute_confidence(ups[brand], downs[brand])

    ranked_popularity = [(popularity, brand) for (brand, popularity) in popDict.items()]
    ranked_popularity.sort()
    ranked_popularity.reverse()

    print "-----ranking_brand_popularity ... "

    result = [(brand, popularity) for (popularity, brand) in ranked_popularity[0:len(ranked_popularity)]]

    print "-----output brand_popularity ... "

    out = file(brand_popularity_file, 'w')
    for (brand, popularity) in result[0:len(result)]:
        out.write('%s %f\n' % (brand, popularity))

    print "-----Ending ... "

    return result

def main():
    compute_brand_popularity("format_data.csv", "brand_popularity.txt")
                                 
if __name__ == "__main__":
    main()
    
