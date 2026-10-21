class BookManager:
    def __init__(self, db):
        self.coll = db["books"]

    def add_book(self, book_doc):
        res = self.coll.insert_one(book_doc)
        print(f"✅ 新增图书，插入id: {res.inserted_id}")
        return res

    def add_books_batch(self, book_list):
        res = self.coll.insert_many(book_list)
        print(f"✅ 批量新增，共插入 {len(res.inserted_ids)} 本")
        return res

    def get_book_by_isbn(self, isbn):
        doc = self.coll.find_one({"isbn": isbn})
        if not doc:
            print("❌ 没有找到这本书")
        return doc

    def search_books(self, cond):
        return list(self.coll.find(cond))

    def update_book(self, isbn, update_data):
        res = self.coll.update_one({"isbn": isbn}, {"$set": update_data})
        print(f"✅ 修改：匹配{res.matched_count}条，实际修改{res.modified_count}条")
        return res

    def update_book_stock(self, isbn, add_stock):
        res = self.coll.update_one({"isbn": isbn}, {"$inc": {"stock": add_stock}})
        print(f"✅ 库存更新：匹配{res.matched_count}条，修改{res.modified_count}条")
        return res

    def delete_book_by_isbn(self, isbn):
        res = self.coll.delete_one({"isbn": isbn})
        print(f"✅ 删除：成功删除 {res.deleted_count} 本")
        return res

    def delete_books_by_category(self, category):
        res = self.coll.delete_many({"category": category})
        print(f"✅ 批量删除【{category}】，共删 {res.deleted_count} 本")
        return res

    def sort_book_by_score(self):
        return list(self.coll.find().sort("score", -1))

# 测试入口
if __name__ == "__main__":
    from mongodb_connect import get_db
    db, client = get_db()
    bm = BookManager(db)
    res = bm.get_book_by_isbn("9787111641247")
    if res:
        print("查到图书：", res)
