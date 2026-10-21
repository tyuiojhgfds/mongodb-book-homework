class StatManager:
    def __init__(self, db):
        self.db = db
        self.book_coll = db["books"]
        self.borrow_coll = db["borrow_logs"]

    def stat_by_category(self):
        # 分类统计：库存总量、平均价格、图书数量，库存降序
        pipeline = [
            {
                "$group": {
                    "_id": "$category",
                    "book_count": {"$sum": 1},
                    "total_stock": {"$sum": "$stock"},
                    "avg_price": {"$avg": "$price"}
                }
            },
            {"$sort": {"total_stock": -1}}
        ]
        return list(self.book_coll.aggregate(pipeline))

    def stat_borrow_trend(self):
        # 按年份统计借阅量
        pipeline = [
            {
                "$group": {
                    "_id": {"$year": "$borrow_time"},
                    "borrow_num": {"$sum": 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        return list(self.borrow_coll.aggregate(pipeline))

    def stat_top_sale(self, top_n=5):
        # 畅销榜：借阅最多的图书
        pipeline = [
            {"$group": {"_id": "$book_isbn", "borrow_cnt": {"$sum": 1}}},
            {"$sort": {"borrow_cnt": -1}},
            {"$limit": top_n}
        ]
        return list(self.borrow_coll.aggregate(pipeline))

if __name__ == "__main__":
    from mongodb_connect import get_db
    db, client = get_db()
    sm = StatManager(db)
    print("分类统计：", sm.stat_by_category())
