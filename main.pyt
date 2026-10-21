from mongodb_connect import get_db
from book_manager import BookManager
from reader_manager import ReaderManager
from borrow_manager import BorrowManager
from stat_manager import StatManager

def main():
    db, client = get_db()
    bm = BookManager(db)
    rm = ReaderManager(db)
    brm = BorrowManager(db)
    sm = StatManager(db)

    # 启动打印连接状态、集合总数
    print("="*50)
    print("📚 图书管理系统启动")
    print("✅ 数据库连接成功")
    print(f"图书总数：{bm.coll.count_documents({})}")
    print(f"读者总数：{rm.coll.count_documents({})}")
    print(f"借阅日志总数：{brm.coll.count_documents({})}")
    print("="*50)

    while True:
        print("\n===== 功能菜单 =====")
        print("1. 新增图书")
        print("2. 按ISBN查询图书")
        print("3. 修改图书信息")
        print("4. 删除图书(单本)")
        print("5. 按分类批量删除图书")
        print("6. 查询读者、统计读者信息")
        print("7. 借阅登记")
        print("8. 图书归还处理")
        print("9. 查询逾期记录")
        print("10. 分类统计（聚合）")
        print("11. 借阅趋势+畅销榜")
        print("0. 退出系统")
        opt = input("请输入功能编号：")

        if opt == "1":
            isbn = input("ISBN：")
            title = input("书名：")
            cate = input("分类：")
            price = float(input("价格："))
            stock = int(input("库存："))
            bm.add_book({"isbn":isbn,"title":title,"category":cate,"price":price,"stock":stock})

        elif opt == "2":
            isbn = input("输入ISBN：")
            res = bm.get_book_by_isbn(isbn)
            if res:
                print(res)

        elif opt == "3":
            isbn = input("要修改的ISBN：")
            new_title = input("新书名：")
            bm.update_book(isbn, {"title": new_title})

        elif opt == "4":
            isbn = input("输入要删除的ISBN：")
            bm.delete_book_by_isbn(isbn)

        elif opt == "5":
            cate = input("输入要清空的分类：")
            bm.delete_books_by_category(cate)

        elif opt == "6":
            print("所有学院：", rm.get_distinct_college())
            print("读者等级分布：", rm.stat_level_distribution())

        elif opt == "7":
            bid = input("图书ISBN：")
            rid = input("读者id：")
            brm.borrow_book({"book_isbn":bid, "reader_id":rid, "borrow_time":"2026-10-21", "returned":False})

        elif opt == "8":
            # 注意：这里输入日志的 _id，需要是ObjectId，仅作业演示
            log_id = input("输入借阅日志_id：")
            brm.return_book(log_id)

        elif opt == "9":
            overdue = brm.query_overdue()
            if len(overdue) == 0:
                print("✅ 没有逾期记录")
            else:
                for item in overdue:
                    print(item)

        elif opt == "10":
            data = sm.stat_by_category()
            for d in data:
                print(d)

        elif opt == "11":
            print("---借阅趋势---")
            trend = sm.stat_borrow_trend()
            for t in trend:
                print(t)
            print("---畅销Top5---")
            top = sm.stat_top_sale(5)
            for t in top:
                print(t)

        elif opt == "0":
            print("🔌 关闭数据库连接，程序退出！")
            client.close()
            break
        else:
            print("❌ 输入无效，请重新选择！")

if __name__ == "__main__":
    main()
