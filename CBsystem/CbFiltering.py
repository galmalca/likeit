import json

class CbFiltering:


    def openFile(filePath):
        with open(filePath) as data_file:
            movies_df = json.load(data_file)
        # print(movies_df[600])
        return (movies_df)


    def algo(comparableItem, dataFrames):
        list = []
        bestScore = 0
        for movie in dataFrames:
            if movie['movieId'] != comparableItem['movieId']:
                matchScore = 0
                for j in range(len(comparableItem['genres'])):
                    for i in range(len(movie['genres'])):
                        if comparableItem['genres'][j] == movie['genres'][i]:
                            matchScore += 1
                        if matchScore > bestScore:
                            bestMatch = movie
                            bestScore = matchScore
                        if matchScore > 1 and len(movie['genres']) <= len(comparableItem['genres']) + 1:
                            list.append(movie)
                        #     list.append(bestMatch)
                        #     return bestMatch
        return list


    def convert_file(filePath):
        with open(filePath) as data_file:
            data = json.load(data_file)

        for item in data:
            str = item['genres']
            wards = str.split(',')
            item['genres'] = wards

        with open(filePath, 'w') as outfile:
            json.dump(data, outfile)
