第五周作業是實作資料庫，使用MYSQL，從安裝server到導出資料庫的實作。

### 技術棧 (Tech Stack)
- 資料庫: MySQL 8.4
### 資料表模型
```
member(1)---(N)message
```

### task1
完成安裝
### task2
建立資料表 member，預覽結果: 
```mysql
CREATE TABLE member (
id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,
name VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
follower_count INT UNSIGNED NOT NULL DEFAULT 0,
time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```
![預覽結果](attachment/Pasted image 260709234553.png)

### task3
###### 1. 插入: 1+4筆資料，並預覽結果(選取全部表格):
```mysql
INSERT INTO member (name, email, password)
VALUE ("test", "test@test.com", "test");
--
INSERT INTO member (name, email, password)
VALUES
("chen", "chen@google.com", "123456");
("peng", "peng@google.com", "999"),
("lee", "lee@test.com", "qwert"),
("lulu", "lulu@google.com", "987654");
--
SELECT * FROM member;
```
![預覽結果](attachment/Pasted%20image%20260709234631.png)

###### 2. 選取表格: ==依照==時間降序排列
```mysql
SELECT * FROM member ORDER BY time DESC;
```
![預覽結果](attachment/Pasted%20image%20260709234755.png)

###### 3. 選取表格: ==依照==時間降序排列+選三並從二到四
```mysql
SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;
```
![預覽結果](attachment/Pasted%20image%20260709234826.png)

###### 4. 選取表格: ==限制條件==email = "---"
```mysql
SELECT * FROM member WHERE email = "test@test.com";
```
![預覽結果](attachment/Pasted%20image%20260709234945.png)
###### 6.選取表格: ==限制條件==email = "---" 並且 密碼="---"
```mysql
SELECT * FROM member WHERE email = "test@test.com" AND password="test";
```
![預覽結果](attachment/Pasted%20image%20260709235023.png)
###### 5.選取表格: ==限制條件==email 包含 es
```mysql
SELECT * FROM member WHERE name LIKE "%es%";
```
![預覽結果](attachment/Pasted%20image%20260709234956.png)

###### 7.更新資料name，==限制條件==email = "---"
```mysql
UPDATE member SET name = "test2" WHERE email = "test@test.com";
```

### task4
使用計算功能
###### 1.(補充)更新資料 follower_count，以利後續計算，並選取全部表格(預覽)
```mysql
UPDATE member SET follower_count = 100 WHERE id = 2;
UPDATE member SET follower_count = 200 WHERE id = 3;
UPDATE member SET follower_count = 800 WHERE id = 4;
UPDATE member SET follower_count = 50 WHERE id = 5;
```
![預覽結果](attachment/Pasted%20image%20260709234653.png)

###### 2. 幾筆資料
```mysql
SELECT COUNT(*) FROM member;
```
![預覽結果](attachment/Pasted%20image%20260709235116.png)
###### 3. 總和(follower_count)
```mysql
SELECT SUM(follower_count) FROM member;
```
![預覽結果](attachment/Pasted%20image%20260709235103.png)
###### 3. 平均(follower_count)
```mysql
SELECT AVG(follower_count) FROM member;
```
![預覽結果](attachment/Pasted%20image%20260709235141.png)
###### 4. 平均(follower_count)，從==依照==時間降序排列前兩個
```mysql
SELECT AVG(follower_count) FROM (
SELECT follower_count FROM member ORDER BY follower_count DESC
LIMIT 2) AS first_two_avg;
```
![預覽結果](attachment/Pasted%20image%20260709235211.png)
### task5
建立另一個表格message，設置FOREIGN KEY。如此，可以從message中的member_id，取得member的資料。
###### 1. 建立表格message，並插入資料
```mysql
CREATE TABLE message(
id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,
member_id INT UNSIGNED NOT NULL,
content TEXT NOT NULL,
like_count INT UNSIGNED NOT NULL DEFAULT 0,
FOREIGN KEY (member_id) REFERENCES member(id)
);

INSERT INTO message (member_id, content, like_count) VALUES
(1, "Good morning", 5),
(1, "Good job", 88),
(3, "Have a good day", 5),
(5, "Fijne Vakantie",3);

SELECT message.*, member.name FROM message JOIN member 
ON message.member_id = member.id;
```
![預覽結果](attachment/Pasted%20image%20260709235312.png)
###### 2. 選取表格: message+member.name(sender names)，==限制條件==email = "---"
```mysql
SELECT message.*, member.name FROM message JOIN member 
ON message.member_id = member.id
WHERE member.email = "test@test.com";
```
![預覽結果](attachment/Pasted%20image%20260709235406.png)
###### 3. 選取表格: avg(like_count)，==限制條件==email = "---"
```mysql
SELECT AVG(message.like_count) FROM message JOIN member 
ON message.member_id = member.id
WHERE member.email = "test@test.com";
```

![預覽結果](attachment/Pasted%20image%20260710000019.png)

###### 4. 選取表格: avg(like_count)，分組
```mysql
SELECT member.email, AVG(message.like_count) FROM message JOIN member 
ON message.member_id = member.id
GROUP BY member.email;
```
![預覽結果](attachment/Pasted%20image%20260710000003.png)

###### 5. 在CMD裡，執行
```
"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqldump.exe"
mysqldump -u root -p website > data.sql
```
### 檢討與回顧
我總結在作業過程中幾個有用的tips:
- 印出(選取表格)可視化表格
- 手畫可視化表格(關聯圖)，比較不容易迷失在各個名稱裡
- 理解問題後，拆解成要顯示甚麼欄位，條件是甚麼
