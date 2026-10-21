class BorrowManager:
    def __init__(self, db):
        self.coll = db["borrow_logs"]

    def borrow_book(self, log_doc):
        res = self.coll.insert_one(log_doc)
        print(f"✅ 借阅登记成功，日志id: {res.inserted_id}")
        return res

    def return_book(self, log_id):
        res = self.coll.update_one(
            {"_id": log_id},
            {"$set": {"returned": True, "return_time": "2026-10-21"}}
        )
        print(f"✅ 归还处理：匹配{res.matched_count}条，修改{res.modified_count}条")
        return res

    def query_overdue(self):
        # 逾期查询示例，根据你的时间字段调整
        cond = {"returned": False}
        return list(self.coll.find(cond))

if __name__ == "__main__":
    from mongodb_connect import get_db
    db, client = get_db()
    brm = BorrowManager(db)
    print("逾期借阅：", brm.query_overdue())
