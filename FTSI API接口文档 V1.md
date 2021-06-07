# 1. FTSI管理后台API接口文档

## 1.1. API V1 接口说明

- 接口基准地址：`http://127.0.0.0:8888/api/`
- API V1 认证统一使用 Token 认证
- 需要授权的 API ，必须在请求头中使用 `Authorization` 字段提供 `token` 令牌
- 使用 HTTP Status Code 标识状态
- 数据返回格式统一使用 JSON

### 1.1.1. 支持的请求方法

- GET（SELECT）：从服务器取出资源（一项或多项）。
- POST（CREATE）：在服务器新建一个资源。
- PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
- DELETE（DELETE）：从服务器删除资源。

### 1.1.2. 通用返回状态说明

| *状态码* | *含义*                | *说明*                               |
| -------- | --------------------- | ------------------------------------ |
| 200      | OK                    | 请求成功                             |
| 201      | CREATED               | 创建成功                             |
| 204      | DELETED               | 删除成功                             |
| 400      | BAD REQUEST           | 请求的地址不存在或者包含不支持的参数 |
| 401      | UNAUTHORIZED          | 未授权                               |
| 403      | FORBIDDEN             | 被禁止访问                           |
| 404      | NOT FOUND             | 请求的资源不存在                     |
| 500      | INTERNAL SERVER ERROR | 内部错误                             |
|          |                       |                                      |

## 1.2. 登录

### 1.2.1. 登录验证接口

- 请求路径：login/userLogin/
- 请求方法：post
- 请求参数

| 参数名   | 参数说明 | 备注     |
| -------- | -------- | -------- |
| username | 用户名   | 不能为空 |
| password | 密码     | 不能为空 |

- 响应参数

| 参数名 | 参数说明 | 备注            |
| ------ | -------- | --------------- |
| token  | 令牌     | 基于 jwt 的令牌 |

- 响应数据

```json
{
  "data": {
  "token": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjExNDEyNTg1LCJlbWFpbCI6Imhhb3llLm1hQGdlLmNvbSJ9.d-6pxIrUpJPvoKS6Wdu_2lKh691ETYLihnjVC0j0Gdk"
}, 
 "meta": {
   "status": 200, 
   "msg": "Login successfully"
 }
}

```

## 1.3. Welcome界面

### 1.3.1. 左侧菜单权限

- 请求路径：common/menus/
- 请求方法：get
- 响应数据

```json
{
  "data": [
    {"id": 101,
     "authName": "FTSI Manage", 
     "path": "", 
     "children": [
       {"id": 102, 
        "authName": "FTSI List", 
        "path": "ftsilist", 
        "children": []}]}, 
    {"id": 201, 
     "authName": "FTSI Operation", 
     "path": "", 
     "children": [
       {"id": 202, 
        "authName": "Task Query", 
        "path": "taskquery", 
        "children": []}
     ], 
  "meta": {
    "msg": "Obtain the menus successfully.", 
    "status": 200}
    }
```

### 1.3.2. Welcome界面中的发动机信息表

- 请求路径：common/engineInfo/
- 请求方法：get

- 响应数据

```json
{
  "data": [
    {"engine": 600101, 
     "aircraft": "AC10101", 
     "left_right": "R", 
     "flight_day": 241, 
     "flight_time": 767.2, 
     "run_time": 975.89, 
     "c1_cycle": 1853, 
     "flight_cycle": 771, 
     "engine_starts": 587, 
     "reverse_cycle": 268}
    ]
  "meta": {
    "meg": "obtain the engine information successfully", 
    "status": 200}
}
```

## 1.4. FTSI Manage

### 1.4.1. FTSI列表

- 请求路径：ftsiMgr/getFTSI/
- 请求方法：get
- 请求参数

| 参数名   | 参数说明     | 备注     |
| -------- | ------------ | -------- |
| query    | 查询参数     | 可以为空 |
| pagenum  | 当前页码     | 不能为空 |
| pagesize | 每页显示条数 | 不能为空 |

- 响应参数

| 参数名     | 参数说明     | 备注 |
| ---------- | ------------ | ---- |
| totalitems | 总记录数     |      |
| pagenum    | 当前页码     |      |
| ftsi_info  | 用户数据集合 |      |

- 响应数据

```json
{
  "data": {
    "totalitems": 3, 
    "pagenum": "1", 
    "ftsi_info": [
      {"id": 11, 
       "ftsi_num": "3001", 
       "rev": "A", 
       "ftsi_title": "TEST-FTSI-001", 
       "statement": "every 50 flight days", 
       "active_status": true, 
       "dep_type": "Up to flight day", 
       "period": "50", 
       "total_times": 999}, 
      {"id": 12, 
       "ftsi_num": "3002", 
       "rev": "A", 
       "ftsi_title": "TEST-FTSI=002", 
       "statement": "every 20 engine hours", 
       "active_status": true, 
       "dep_type": "Up to engine hour", 
       "period": "20", 
       "total_times": 999}, 
      {"id": 13, 
       "ftsi_num": "3003", 
       "rev": "A", 
       "ftsi_title": "TEST-FTSI-003", 
       "statement": "active by 3002, every 10 flight days 2 times, then every 50 engine hours.", 
       "active_status": true, 
       "dep_type": "Customize", 
       "period": "", 
       "total_times": 1}
    ]
  }, 
  "meta": {
    "msg": "obtain the ftsi information successfully", 
    "status": 200
  }
}
```

### 1.4.2.Monitor Type下拉菜单的权限

- 请求路径：ftsiMgr/paraforAddFTSI/
- 请求方法：get
- 响应数据

```json
{
  "data": {
    "monitorType": [
      ["OTHER", "On condition"], 
      ["FD", "Up to flight day"], 
      ["FH", "Up to flight hour"], 
      ["EH", "Up to engine hour"], 
      ["CC", "Up to C1 cycle"], 
      ["DATE", "Up to date"], 
      ["FC", "Up to flight cycle"], 
      ["ES", "Up to engine starts"], 
      ["RC", "Up to reverse cycle"], 
      ["CUS", "Customize"]
    ], 
    "triggerType": [
      ["NA", "No active item"], 
      ["TDATE", "Active by date"], 
      ["TFTSI", "Active by FTSI"]
    ]
  }, 
 "meta": {
   "msg": "obtain the types successfully", 
   "status": 200}
}
```

### 1.4.3.验证FTSI number是否已经存在于数据库中

- 请求路径：ftsiMgr/FTSInumExistCheck/
- 请求方法：get

- 请求参数

| 参数名   | 参数说明 | 备注     |
| -------- | -------- | -------- |
| ftsi_num | 查询参数 | 可以为空 |

- 响应数据

```json
{
  "data": {}, 
  "meta": {
    "msg": "validation pass", 
    "status": 200}
}
```

### 1.4.3. 添加新的FTSI

- 请求路径：ftsiMgr/addFTSI/
- 请求方法：post
- 请求参数

| 参数名        | 参数说明                         | 备注     |
| :------------ | :------------------------------- | :------- |
| FTSI_num      | FTSI number                      | 不能为空 |
| revision      | FTSI revision                    | 不能为空 |
| FTSI_title    | FTSI title                       | 可以为空 |
| compliance    | Compliance statement             | 可以为空 |
| type          | Period type (FD FH On condition) | 不能为空 |
| period        | 两次执行的间隔                   | 可以为空 |
| times         | 合计的执行次数                   | 不能为空 |
| appliedIPS    | 适用该FTSI的IPS                  | 不能为空 |
| customizePara | 当类型为CUS时的补充参数          |          |

- 请求参数例子

```json
    "ftsi_num": "3004", 
    "rev": "A", 
    "ftsi_title": "TEST-FTSI-004", 
    "statement": "10 flight days for first inspection, then every 50 engine hours", 
    "dep_type": "CUS", 
    "period": "", 
    "total_times": "1", 
    "appliedIPS": [600101, 600102, 600103, 600104, 600105, 600106, 600108, 600109, 600110, 600111, 600112, 600114, 600115], 
    "customizePara": {
      "trigger": {"type": "NA", "parameter": ""}, 
      "monitorParam": [{"type": "FD", "period": "10", "times": "1"},
        {"type": "EH", "period": "50", "times": "999"}]
    }
```

- 响应数据

```json
{
  "data": {}, 
  "meta": {
    "msg": "Add a new FTSI successfully!", 
    "status": 201}
}
```

### 1.4.4. 获取特定FTSI下的特定信息

- 请求路径：ftsiMgr/getFTSIInfo/
- 请求方法：GET
- 请求参数

| 参数名 | 参数说明       | 备注     |
| :----- | :------------- | :------- |
| id     | FTSI号对应的ID | 不能为空 |

- 响应数据

```json
{
  "data": {
    "id": 13, 
    "ftsi_num": "3003", 
    "rev": "A", 
    "ftsi_title": "TEST-FTSI-003", 
    "statement": "active by 3002, every 10 flight days 2 times, then every 50 engine hours.", 
    "active_status": true, 
    "dep_type": "CUS", 
    "period": "", 
    "total_times": 1, 
    "appliedIPS": [600101, 600102, 600103, 600104, 600105, 600106, 600107, 600108], 
    "customizePara": {
      "trigger": {"type": "TFTSI", "parameter": "3002"}, 
      "monitorParam": [{"type": "FD", "period": "10", "times": 2}, 
        {"type": "EH", "period": "50", "times": 999}]
    }
  }, 
  "meta": {
    "msg": "obtain the ftsi information successfully", 
    "status": 200
  }
}
```

### 1.4.5. 编辑FTSI的信息

- 请求路径：ftsiMgr/editFTSI/
- 请求方法：PUT
- 请求参数

| 参数名        | 参数说明                            | 备注     |
| :------------ | :---------------------------------- | :------- |
| FTSI_num      | FTSI number                         | 不能为空 |
| revision      | FTSI revision                       | 不能为空 |
| FTSI_title    | FTSI title                          | 可以为空 |
| compliance    | Compliance statement                | 可以为空 |
| type          | Period type (FD FH On condition)    | 不能为空 |
| period        | 两次执行的间隔                      | 可以为空 |
| times         | 合计的执行次数                      | 不能为空 |
| appliedIPS    | 适用该FTSI的IPS                     | 不能为空 |
| customizePara | 当类型为CUS时的补充参数             |          |
| modifyType    | True/False 是否有关于监控参数的修改 | 不能为空 |
| modifyRange   | True/False 是否有IPS范围修改        | 不能为空 |

- 请求参数例子

```json
"id": 11, 
"ftsi_num": "3001", 
"rev": "A", 
"ftsi_title": "TEST-FTSI-001", 
"statement": "every 50 flight days", 
"active_status": true, 
"dep_type": "FD", 
"period": "50", 
"total_times": 999, 
"appliedIPS": [600101, 600102, 600103, 600104, 600105, 600106, 600107, 600108, 600109, 600110, 600111, 600112, 600113, 600114, 600115], 
"customizePara": {
  "trigger": {"type": "NA", "parameter": ""}, 
  "monitorParam": [{"type": "", "period": "", "times": ""}]}, 
"modifyType": false, 
"modifyRange": false
```

- 响应数据

```json
{
  "data": {}, 
  "meta": {
    "msg": "Modify the FTSI information successfully", 
    "status": 200
  }
}
```

### 1.4.6. FTSI文件升版

- 请求路径：ftsiMgr/updateFTSI/
- 请求方法：PUT
- 请求参数

| 参数名        | 参数说明                            | 备注     |
| :------------ | :---------------------------------- | :------- |
| FTSI_num      | FTSI number                         | 不能为空 |
| revision      | FTSI revision                       | 不能为空 |
| FTSI_title    | FTSI title                          | 可以为空 |
| compliance    | Compliance statement                | 可以为空 |
| type          | Period type (FD FH On condition)    | 不能为空 |
| period        | 两次执行的间隔                      | 可以为空 |
| times         | 合计的执行次数                      | 不能为空 |
| appliedIPS    | 适用该FTSI的IPS                     | 不能为空 |
| customizePara | 当类型为CUS时的补充参数             |          |
| modifyType    | True/False 是否有关于监控参数的修改 | 不能为空 |
| modifyRange   | True/False 是否有IPS范围修改        | 不能为空 |

- 请求参数例子

```json
"id": 11, 
"ftsi_num": "3001", 
"rev": "A", 
"ftsi_title": "TEST-FTSI-001", 
"statement": "every 50 flight days", 
"active_status": true, 
"dep_type": "FD", 
"period": "50", 
"total_times": 999, 
"appliedIPS": [600101, 600102, 600103, 600104, 600105, 600106, 600107, 600108, 600109, 600110, 600111, 600112, 600113, 600114, 600115], 
"customizePara": {
  "trigger": {"type": "NA", "parameter": ""}, 
  "monitorParam": [{"type": "", "period": "", "times": ""}]}, 
"modifyType": false, 
"modifyRange": false
```

- 响应数据

```json
{
  "data": {}, 
  "meta": {
    "msg": "Update the FTSI version successfully", 
    "status": 200
  }
}
```

### 1.4.7. 查询FTSI下适用的IPS

- 请求路径：ftsiMgr/detailFTSI/
- 请求方法：get
- 请求参数

| 参数名 | 参数说明      | 备注     |
| ------ | ------------- | -------- |
| id     | FTSI下ips的ID | 不能为空 |

- 响应数据

```json
{
  "data": {
    "FTSI": {"id": 15, 
             "ftsi_num": "3006", 
             "rev": "A", 
             "ftsi_title": "TEST FTSI 0006", 
             "statement": "every 90 flight hours", 
             "active_status": true, 
             "dep_type": "FH", 
             "period": "90", 
             "total_times": 999}, 
    "ipsDetail": [
      {"id": 161, 
       "ftsi_id": 15, 
       "engine_id": 600101, 
       "last_date": "new created", 
       "current_type": "Up to flight hour", 
       "next_target": "857.2", 
       "residual_times": 999, 
       "active_status": true}, 
      {"id": 162, 
       "ftsi_id": 15, 
       "engine_id": 600102, 
       "last_date": "new created", 
       "current_type": "Up to flight hour", 
       "next_target": "383.37", 
       "residual_times": 999, 
       "active_status": true}
    ]
  }, 
  "meta": {
    "msg": "Obtain the IPS list for this FTSI successfully", 
    "status": 200
  }
}
```

### 1.4.7. 修改FTSI_IPS的开关状态

- 请求路径：ftsiMgr/detailFTSI/statusChange/
- 请求方法：PUT
- 请求参数

| 参数名        | 参数说明              | 备注     |
| ------------- | --------------------- | -------- |
| id            | FTSI_IPS的id          | 不能为空 |
| active_status | True/False 开关的状态 | 不能为空 |

- 响应数据

```json
{
  "data": {}, 
  "meta": {
    "msg": "update the status of the applied IPS successfully!", 
    "status": 200
  }
}
```

### 1.4.8. 获取FTSI_IPS的具体信息

- 请求路径：ftsiMgr/detailFTSI/statusChange/
- 请求方法：GET
- 请求参数

| 参数名 | 参数说明     | 备注     |
| ------ | ------------ | -------- |
| id     | FTSI_IPS的id | 不能为空 |

- 响应数据

```json
{
  "data": {
  "id": "138", 
    "ftsi_num": "3003", 
    "ftsi_title": "TEST-FTSI-003", 
    "statement": "active by 3002, every 10 flight days 2 times, then every 50 engine hours.", 
    "dep_type": "Customize", 
    "engine_id": 600101, 
    "last_date": "new created", 
    "current_type": "trigger_factor", 
    "active_status": true, 
    "next_target": "After 3002", 
    "residual_times": null, 
    "DB_keyword": "", 
    "unit": "", 
    "engine_info": {
      "engine": 600101, 
      "aircraft": "AC10101", 
      "left_right": "R", 
      "flight_day": 241, 
      "flight_time": 767.2, 
      "run_time": 975.89, 
      "c1_cycle": 1853, 
      "flight_cycle": 771, 
      "engine_starts": 587, 
      "reverse_cycle": 268
    }, 
    "customize": {
      "trigger_factor": {"type_label": "TFTSI", 
                         "type_value": "trigger_factor", 
                         "trigger_par": "3002", 
                         "DB_keyword": "", 
                         "unit": ""}, 
      "dep_type1": {"type_label": "FD", 
                    "type_value": "dep_type1", 
                    "period": "10", 
                    "total_times": 2, 
                    "DB_keyword": 
                    "flight_day", 
                    "unit": "FD"}, 
      "dep_type2": {"type_label": "EH", 
                    "type_value": "dep_type2", 
                    "period": "50", 
                    "total_times": 999, 
                    "DB_keyword": "run_time", 
                    "unit": "EH"}
    }
  }, 
  "meta": {
    "msg": "Obtain the FTSI_IPS information successfully!", 
    "status": 200
  }
}
```

### 1.4.9. 编辑FTSI_IPS的信息

- 请求路径：ftsiMgr/detailFTSI/infoChange/
- 请求方法：PUT
- 请求参数：为1.4.8中响应数据的data部分

- 请求方法：get
- 响应数据

```json
{
  "data": {}, 
  "meta": {
    "msg": "Modify the FTSI-IPS information successfully!", 
    "status": 200
  }
}
```



## 1.5. FTSI Operation

### 1.5.1. 上方选择菜单权限

- 请求路径：ftsiOpt/selectBar/
- 请求方法：GET
- 响应数据

```json
{
  "data": {
    "aircraft_list": ["AC10101", "AC10102", "AC10103", "AC10104", "AC10105", "AC10106"], 
    "type_list": ["All", "Parameter dependence", "On condition", "Unactive"]
  }, 
  "meta": {
    "msg": "obtain the select bar successfully", 
    "status": 200
  }
}
```

### 1.5.2. 左右发所对应的FTSI

- 请求路径：ftsiOpt/ftsiforAircraft/
- 请求方法：GET
- 请求参数

| 参数名      | 参数说明   | 备注     |
| ----------- | ---------- | -------- |
| aircraftMSN | 飞机编号   | 不能为空 |
| monitorType | 监控类型   | 可以为空 |
| Select      | 查找域     | 可以为空 |
| Input       | 查找关键词 | 可以为空 |

- 响应数据

```json
{
  "data": {
    "leftIPS": {"engine": 600104, 
                "aircraft": "AC10101", 
                "left_right": "L", 
                "flight_day": 241, 
                "flight_time": 767.2, 
                "run_time": 1009.76, 
                "c1_cycle": 1885, 
                "flight_cycle": 771, 
                "engine_starts": 612, 
                "reverse_cycle": 269}, 
    "rightIPS": {"engine": 600101, "aircraft": "AC10101", "left_right": "R", "flight_day": 241, "flight_time": 767.2, "run_time": 975.89, "c1_cycle": 1853, "flight_cycle": 771, "engine_starts": 587, "reverse_cycle": 268}, 
    "amountLeft": 5, 
    "amountRight": 5,
    "ftsiForLeft": [
      {"id": 111, 
       "ftsi_id": 18, 
       "engine_id": 600104, 
       "last_date": "new created", 
       "current_type": "FD", 
       "next_target": "291", 
       "residual_times": 999, 
       "active_status": true, 
       "ftsi_info": {
         "id": 18, 
         "ftsi_num": "3001", 
         "rev": "C", 
         "ftsi_title": "TEST-FTSI-001", 
         "statement": "every 50 flight days", 
         "active_status": true, 
         "dep_type": "FD", 
         "period": "50", 
         "total_times": 999},
       "comments": "50 FD left, \nnext 291 FD", 
       "reminds": "safe"},
      {"id": 126, "ftsi_id": 17, "engine_id": 600104, "last_date": "new created", "current_type": "EH", "next_target": "1029.76", "residual_times": 999, "active_status": true, "ftsi_info": {"id": 17, "ftsi_num": "3002", "rev": "B", "ftsi_title": "TEST-FTSI=002", "statement": "every 20 engine hours", "active_status": true, "dep_type": "EH", "period": "20", "total_times": 999}, "comments": "20.0 EH left, \nnext 1029.76 EH", "reminds": "safe"}], 
    "ftsiForRight": [
      {"id": 108, "ftsi_id": 18, "engine_id": 600101, "last_date": "new created", "current_type": "FD", "next_target": "291", "residual_times": 999, "active_status": true, "ftsi_info": {"id": 18, "ftsi_num": "3001", "rev": "C", "ftsi_title": "TEST-FTSI-001", "statement": "every 50 flight days", "active_status": true, "dep_type": "FD", "period": "50", "total_times": 999}, "comments": "50 FD left, \nnext 291 FD", "reminds": "safe"}]
  }, 
  "meta": {
    "msg": "Obtain the FTSI info for the selected MSN successfully", 
    "status": 200
  }
}
```

### 1.5.3. 预测给定飞行参数下可能需要执行文件的列表

- 请求路径：ftsiOpt/selectBar/
- 请求方法：GET

- 请求参数

| 参数名      | 参数说明         | 备注     |
| ----------- | ---------------- | -------- |
| aircraftMSN | 飞机编号         | 不能为空 |
| flightDay   | 飞行日数         | 不能为空 |
| flightHour  | 飞行小时数       | 不能为空 |
| engineHour  | 发动机运行小时数 | 不能为空 |
| c1Cycle     | C1循环数         | 不能为空 |

- 响应数据

```json
{
  "data": {
    "leftIPS": {"engine": 600104, "aircraft": "AC10101", "left_right": "L", "flight_day": 241, "flight_time": 767.2, "run_time": 1009.76, "c1_cycle": 1885, "flight_cycle": 771, "engine_starts": 612, "reverse_cycle": 269}, 
    "rightIPS": {"engine": 600101, "aircraft": "AC10101", "left_right": "R", "flight_day": 241, "flight_time": 767.2, "run_time": 975.89, "c1_cycle": 1853, "flight_cycle": 771, "engine_starts": 587, "reverse_cycle": 268}, 
    "ftsiForLeft": [
      {"id": 111, 
       "ftsi_id": 18, 
       "engine_id": 600104, 
       "last_date": "new created", 
       "current_type": "FD", 
       "next_target": "242", 
       "residual_times": 999, 
       "active_status": true, 
       "ftsi_info": {
         "id": 18, 
         "ftsi_num": "3001", 
         "rev": "C", 
         "ftsi_title": "TEST-FTSI-001", 
         "statement": "every 50 flight days", 
         "active_status": true, 
         "dep_type": "FD", 
         "period": "50", 
         "total_times": 999}, 
       "content": "0 FD"}], 
    "ftsiForRight": [
      {"id": 108, "ftsi_id": 18, "engine_id": 600101, "last_date": "new created", "current_type": "FD", "next_target": "242", "residual_times": 999, "active_status": true, "ftsi_info": {"id": 18, "ftsi_num": "3001", "rev": "C", "ftsi_title": "TEST-FTSI-001", "statement": "every 50 flight days", "active_status": true, "dep_type": "FD", "period": "50", "total_times": 999}, "content": "0 FD"}]
  }, 
 "meta": {
   "msg": "obtain the predict results successfully", 
   "status": 200
 }
}
```

### 1.5.4. 获取飞机对应的发动机编号

- 请求路径：ftsiOpt/getEngineNum/
- 请求方法：GET
- 请求参数

| 参数名      | 参数说明 | 备注     |
| ----------- | -------- | -------- |
| aircraftMSN | 飞机编号 | 不能为空 |

- 响应数据

```json
{
  "data": {
    "left_engine": 600111, 
    "right_engine": 600112
  }, 
 "meta": {
   "msg": "obtain the related engines successfully", 
   "status": 200
 }
}
```

### 1.5.5. 检查执行文件后产生的变化信息

- 请求路径：ftsiOpt/checkFTSIinfo/
- 请求方法：GET
- 请求参数

| 参数名        | 参数说明                   | 备注     |
| ------------- | -------------------------- | -------- |
| engineNum     | 发动机编号                 | 不能为空 |
| implementFTSI | 执行的FTSI编号 (用'/'隔开) | 不能为空 |
| implementDate | 执行日期                   | 不能为空 |

- 响应数据

```json
{
  "data": {
    "FTSI_info": [
      {"id": 14, 
       "ftsi_num": "3004", 
       "rev": "A", 
       "ftsi_title": "TEST-FTSI-004", 
       "statement": "at first opportunity", 
       "active_status": true, 
       "dep_type": "OTHER", 
       "period": "", 
       "total_times": 1, 
       "ips_info": {
         "id": 149, 
         "ftsi_id": 14, 
         "engine_id": 600104, 
         "last_date": "new created", 
         "current_type": "OTHER", 
         "next_target": "", 
         "residual_times": 1, 
         "active_status": true}, 
       "comments": "Next: Closed"}, 
      {"id": 17, "ftsi_num": "3002", "rev": "B", "ftsi_title": "TEST-FTSI=002", "statement": "every 20 engine hours", "active_status": true, "dep_type": "EH", "period": "20", "total_times": 999, "ips_info": {"id": 126, "ftsi_id": 17, "engine_id": 600104, "last_date": "new created", "current_type": "EH", "next_target": "1015", "residual_times": 999, "active_status": true}, "comments": "activate '3003'. Next target: 1029.76 EH"}], 
    "warning_info": "FTSI: '3009' is closed or not applied for this engine.<br/>"
  }, 
  "meta": {
    "msg": "obtain the check result successfully", 
    "status": 200
  }
}
```

### 1.5.6. 提交执行的文件编号

- 请求路径：ftsiOpt/submitFTSIinfo/
- 请求方法：PUT
- 请求参数

| 参数名        | 参数说明                   | 备注     |
| ------------- | -------------------------- | -------- |
| engineNum     | 发动机编号                 | 不能为空 |
| implementFTSI | 执行的FTSI编号 (用'/'隔开) | 不能为空 |
| implementDate | 执行日期                   | 不能为空 |

- 响应数据

```json
{
  "data": {
    "warning_info": "FTSI: '3009' is closed or not applied for this engine.<br/>"
  }, 
  "meta": {
    "msg": "submit the implemented FTSI successfully", 
    "status": 200
  }
}
```

### 