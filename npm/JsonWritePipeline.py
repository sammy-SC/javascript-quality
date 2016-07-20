
class JsonWritePipeline(object):
    def __init__(self):
        self.file = open('items.csv', 'a')

    def process_item(self, item, spider):
        line = "{}, {}, {}, {}, {}\n".format(item["title"],
                    item["github"],
                    item["monthly_downloads"],
                    item["weekly_downloads"],
                    item["daily_downloads"])

        self.file.write(line)
        return item
