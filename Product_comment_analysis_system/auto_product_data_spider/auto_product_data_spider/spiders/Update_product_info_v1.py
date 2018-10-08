# Update Product Info
#             if os.path.getsize(settings.product_info_path + "ProductInfoPCAuto.csv"):
#                 product_info = pandas.read_csv(settings.product_info_path + "ProductInfoPCAuto.csv", header=0)
#             else:
#                 product_info = pandas.DataFrame([], columns=self.column_name)
#             if product_name in product_info["Product_Model"].tolist():
#                     row_index = product_info[product_info["Product_Model"] == "奔驰C级"].index.tolist()[0]
#                     product_info.loc[row_index, "CommentNum"] = comment_num
#                     product_info.loc[row_index, "UpdateTime"] = \
#                         time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#             else:
#                 self.product_id += 1
#                 row = [
#                     self.product_id,
#                     response.meta["rootURL_Id"],
#                     product_name,
#                     product_model,
#                     url,
#                     comment_num,
#                     time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
#                     self.user
#                 ]
#                 product_info = product_info.append(row, ignore_index=True)
#             product_info.to_csv(
#                 settings.product_info_path + "ProductInfoPCAuto.csv",
#                 index=0
#             )
