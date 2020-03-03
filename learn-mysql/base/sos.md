### 误删数据
#### 误删行
如果 `binlog_format=row` 和 `binlog_row_image=FULL`， 可以用`Flashback`工具通过闪回把数据恢复。  

使用 `delete` 命令删除的数据还可能通过 `binlog` 恢复，而使用 `truncate/drop table` 和 `drop datebase` 命令删除的数据，就没办法通过
`Flashback`恢复了，因为这些语句，记录在 binlog 中总是 statement 格式的。

##### 预防
- 把 `sql_safe_updates` 参数设置为 `on`， `delete` 或 `update` 语句如果没有`where`条件或`where`条件中没有包含索引字段的话，这条语句就会报错
- 上线前，进行 sql 审计

#### 误删表/库
如果有定期的全量个备份和实时的binlog，可以使用全量备份加增量日志的方式恢复。

##### 预防
- 账号分离，权限明确，只允许应用开发人员使用 DML 语句
- 读取业务，使用只读账号
- 制定操作规范。这样做的目的，是避免写错要删除的表名。 在删除数据表之前，先对表做改名操作，观察对业务无影响后再删除
