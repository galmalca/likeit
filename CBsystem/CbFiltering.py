import json
import random


class CbFiltering:
    def __init__(self):
        pass

    @classmethod
    def openFile(filePath):
        with open(filePath) as data_file:
            dataFrame = json.load(data_file)
        return (dataFrame)

    @classmethod
    def algo(cls, comparableItem, dataFrame):
        list = []
        bestScore = 0
        for item in dataFrame:
            if item['_id'] != comparableItem['_id']:
                matchScore = 0
                for j in range(len(comparableItem['categories'])):
                    for i in range(len(item['categories'])):
                        if comparableItem['categories'][j] == item['categories'][i]:
                            matchScore += 1
                    if matchScore >= bestScore:
                        bestMatch = item
                        bestScore = matchScore
                    if matchScore > 1 and len(item['categories']) <= len(comparableItem['categories']) + 4:
                        list.append(item)
        random.shuffle(list)
        return list[:20]

    @classmethod
    def convert_file(filePath):
        with open(filePath) as data_file:
            data = json.load(data_file)

        for item in data:
            str = item['categories']
            wards = str.split(',')
            item['categories'] = wards

        with open(filePath, 'w') as outfile:
            json.dump(data, outfile)
