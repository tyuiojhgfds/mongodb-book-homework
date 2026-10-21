class ReaderManager:
    def __init__(self, db):
        self.coll = db["readers"]

    def find_reader(self, cond):
        return list(self.coll.find(cond))

    def count_all(self):
        return self.coll.count_documents({})

    def count_by_cond(self, cond):
        return self.coll.count_documents(cond)

    def get_distinct_college(self):
        return self.coll.distinct("college")

    def get_distinct_level(self):
        return self.coll.distinct("level")

    def stat_level_distribution(self):
        pipeline = [
            {"$group": {"_id": "$level", "count": {"$sum": 1}}}
        ]
        return list(self.coll.aggregate(pipeline))

if __name__ == "__main__":
    from mongodb_connect import get_db
    db, client = get_db()
    rm = ReaderManager(db)
    print("所有学院：", rm.get_distinct_college())
