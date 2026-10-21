
from pymongo import MongoClient

def get_db():
    # 统一连接参数
    client = MongoClient("mongodb://localhost:27017/")
    db = client["library_db"]
    return db, client

if __name__ == "__main__":
    db, cli = get_db()
    print("✅ 数据库连接成功，库名：library_db")
