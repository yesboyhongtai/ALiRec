# @fucntion: compute ranking of people in test data according to computed popularity
# @author: Zhang Hongtai
# @date: 2014-03-31

import math
from operator import itemgetter

def compute_ranks_using_popularity(brand_candidate_file, brand_popularity_file, brand_rank_file, brand_recommend_file):
    all_brand_list = []
    
    user_rec_rank = ""
    all_user_rec_rank = []
    rec_brand_list = []
    
    brand_popularity = {}
    all_brand_popularity = {}
    
    brand_ranking = {}
    
    print "reading brand popularity ... "
    
    for line in file(brand_popularity_file):
        line = line[:-1]
        brand_can, popularity = line.split(' ')
        all_brand_popularity[brand_can] = float(popularity)
        
    print "calculating brand recommend ranking ... "
    
    
    for line in file(brand_candidate_file):
        user_rec_rank = ""
        brand_popularity = {}
        brand_ranking = {}

        line = line[:-1]
        brand_rec = all_brand_list = line.split(' ')
        user = all_brand_list[0]
        brand_list = all_brand_list[1:len(all_brand_list)]
        
        for brand in brand_list:
            if brand in all_brand_popularity:
                brand_popularity[brand] = all_brand_popularity[brand]
            else:
                brand_popularity[brand] = 0.0

        ranked_brand_popularity = [(popularity, brand) for (brand, popularity) in brand_popularity.items()]
        ranked_brand_popularity.sort()
        ranked_brand_popularity.reverse()

        ranking = 1
        for (popularity, brand) in ranked_brand_popularity[0:len(ranked_brand_popularity)]:
            brand_ranking[brand] = ranking
            ranking += 1
        
        
        line = 1
        for brand in brand_list:
            if line == 1:
                user_rec_rank += str(brand_ranking[brand])
            else:
                user_rec_rank += " " + str(brand_ranking[brand])
            line += 1
            
            if(brand_ranking[brand] > math.ceil(len(brand_rec)/2.0)):
                brand_rec.remove(brand)
        
        #Output the recommend brand
        
        all_user_rec_rank.append(user_rec_rank)
        str_brand = ','.join(brand_rec)
        str_brand = str_brand.replace(',', '\t', 1)
        rec_brand_list.append(str_brand)
    print "output ranking file ... "
    
    out = file(brand_rank_file, 'w')
    for user_rec_rank in all_user_rec_rank[0:len(all_user_rec_rank)]:
        out.write('%s\n' % (user_rec_rank))
    
    result = file(brand_recommend_file, 'w')
    for brand_rec in rec_brand_list[0:len(rec_brand_list)]:
        result.write('%s\n' % (brand_rec))
    
    print "Ending"
  
    
def main():
    compute_ranks_using_popularity("brand_candidate.txt", "brand_popularity.txt", "brand_rank.txt", "brand_recommend.txt")
                                 
if __name__ == "__main__":
    main()
