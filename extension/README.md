# Database Efficiency Comparison

A simple database efficiency comparison. It compares the write and read efficiency of three types of database: [MySQL](https://www.mysql.com/), [MongoDB](https://www.mongodb.com/) and [ElasticSearch](https://www.elastic.co/), which give us a hint about which database backend we can plug into the Django framework.

The tests conducted include:
1. write: write 1 million paper metadata to the database.
2. query one tag: whether a given *tag* exist, e.g. the full title, the full author lists.
3. query one word: whether the field contains the given word.

Results:
|               | Write     | Querying one field | Querying one datapoint |
|---------------|-----------|--------------------|------------------------|
| MySQL         | 3h 58 min | 0.00015s           | 0.00021s               |
| MongoDB       | 4h 17 min | 0.00024s           | 0.00037s               |
| ElasticSearch | 5h 48 min | 0.00006s           | 0.00010s               |

In the end, we decided to use MySQL because it's one of Django's default database backends, which makes it easier to set up. It's also very convenient to switch to MongoDB backend, but MongoDB is slower in all three experiments than MySQL.