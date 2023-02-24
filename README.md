# Ceramics

The aim of the app is to support teachers providing extra-curricular activities for children.

## Domain

1. Teacher sets up several courses at the beginning of the year

2. Course has a name, start date, end date, day of the week and time when it takes place and price per one lesson

    Example: Ceramics course, every Thursday 5:00pm from Sep 1st until Dec 31st, $30 per student per class

3. Parents of students sign them up for one or more courses, but students are free to attend lessons from other courses as well

    Example: student usually attends a Thursday 5:00pm course, but she is also free to attend Wednesday 4:00pm course
 
4. At every lesson teacher checks the attendance of course students and other students that have attended the lesson from other courses.

5. Parents pay for lessons that student has attended.


## Development

```
pip install -r requirements.txt
pip install -e src/
```

```
docker run -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres
python -c "from ceramics.config import create_schema; create_schema()"
```

```
make up
```
