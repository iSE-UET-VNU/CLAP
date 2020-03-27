Chuẩn bị dữ liệu cho bài toán Configuration-dependent bugs localization

Note:
- Sampling bằng SPLCATool
- Generate Mutants bằng Mujava
Nên cần lưu ý về việc config của SPLCATool và Mujava trước khi chạy

- Configurations cần được generate theo đúng thứ tự của features
- feature_order.txt là files gồm tất cả các features được liệt kê theo đúng thứ tự quy định của model

- model.m là file model ở dạng guiclsl 

Run:
```shell script
$ export ANT_HOME=InputPreparation/plugins/apache-ant-1.10.7/
```

```shell script
$ python Main_MakeDataset.py
```
