import pymysql

# The SQLs
# Insert
insert_into_Info = """insert into
DataProductInfo(RootURL_ID, Product_Name, Product_Model, CommentNum, UpdateTime, User)
values('{}', '{}', '{}', '{}', '{}', '{}')"""
insert_into_Comment = """insert into
DataProductComment(product_ID, Product_Type_ID, Reviewer, Location, Comment,
CommentMedia, CommentTime, Score, ScoreSource, upvote, reviews, UpdateTime, User)
values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"""
# Select
# Query if the product is exist
if_product_in_table = "select 1 from DataProductInfo where Product_Name = '{}' limit 1;"
if_comment_in_table = """select 1 from DataProductComment
where Comment = '{}' and Reviewer = '{}' and CommentTime = '{}' and Location = '{}'
limit 1;
"""
# Query the product id
query_product_id = "select Product_ID from DataProductInfo where Product_Name = '{}'"
# Update
# Update the product information table
update_product_info = """update DataProductInfo
set {} = '{}'
where Product_Name = '{}'
"""
update_product_info2 = """update DataProductInfo
set {} = '{}'
where Product_ID = {}
"""


def connect_database():
    # Create a connection to database
    # connect = pymysql.connect(
    #     user="root",
    #     password="12345678",
    #     database="online_Data",
    #     charset="utf8",
    # )
    connect = pymysql.connect(
        user="root",
        password="12345678",
        database="online_Data",
        charset="utf8",
    )
    connect.autocommit(True)
    cursor = connect.cursor()
    return connect, cursor


def query(cursor, sql):
    cursor.execute(sql)
    result = cursor.fetchone()
    return result
