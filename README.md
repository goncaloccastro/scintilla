# Scintilla

---

Scintilla is a small Python library that makes use of Faker to generate multiple DataFrames 
that can then be used for property based testing.

If you're looking for a library to test DataFrame assertions I recommend using 
the [chispa](https://github.com/MrPowers/chispa) library as it contains several methods to help in comparing DataFrames.

## DataFrame Generator

This module lets you create DataFrames, according to a schema, with fake synthetic data (using Faker) so that 
you can either use it in your tests or make use of property based testing (explained further down).

The starting point is the DataFrameGenerator data class, and it can be created by doing the following:

```python
df_gen: DataFrameGenerator = DataFrameGenerator(schema=schema)
```

Where the schema is a StructType object like the following:

```python
schema: StructType = StructType([
    StructField("expected_name", StringType(), True),
    StructField("int", IntegerType(), True),
    StructField("long", LongType(), True),
    StructField("byte", ByteType(), True),
    StructField("short", ShortType(), True),
    StructField("double", DoubleType(), True),
    StructField("float", FloatType(), True),
    StructField("decimal", DecimalType(), True),
    StructField("bool", BooleanType(), True),
    StructField("binary", BinaryType(), True),
    StructField("date", DateType(), True),
    StructField("timestamp", TimestampType(), True)
])
```

Those are the supported types right now, each of those types has a matching Faker provider in the `DEFAULT_CONFIG` dictionary:

```python
DEFAULT_CONFIG: dict = {
    "StringType": {"provider": "pystr"},
    "ByteType": {"provider": "pyint", "kwargs": {"min_value": -128, "max_value": 127}},
    "ShortType": {"provider": "pyint", "kwargs": {"min_value": -32768, "max_value": 32767}},
    "IntegerType": {"provider": "pyint", "kwargs": {"min_value": -2147483648, "max_value": 2147483647}},
    "LongType": {"provider": "pyint", "kwargs": {"min_value": -9223372036854775808, "max_value": 9223372036854775807}},
    "DoubleType": {"provider": "pyfloat"},
    "FloatType": {"provider": "pyfloat"},
    "DecimalType(10,0)": {"provider": "pydecimal", "kwargs": {"left_digits": 10, "right_digits": 0}},
    "DateType": {"provider": "date_object"},
    "TimestampType": {"provider": "date_time"},
    "BooleanType": {"provider": "pybool"},
    "BinaryType": {"provider": "binary", "kwargs": {"length": 64}}
}
```

Calling the method `arbitrary_dataframes` from the DataFrameGenerator will give you a Python generator of 
DataFrames (default is 10 DataFrames) with rows filled with fake data (default is 10 rows).

For instance, the following code:

```python
schema: StructType = StructType([
    StructField("string", StringType(), True),
    StructField("int", IntegerType(), True),
    StructField("date", DateType(), True)
])
df_gen: DataFrameGenerator = DataFrameGenerator(schema=schema)
for df in df_gen.arbitrary_dataframes():
    df.show()
```

will result in:

```shell
+--------------------+-----------+----------+
|              string|        int|      date|
+--------------------+-----------+----------+
|athKDRmDyDoOFTtMyEpS|  208977570|1998-10-05|
|KsiKWhuWhrxwjIfZObWE|   36536111|2009-02-07|
|yBnbHFvtUaMITurvzgGa|-1150452234|1975-06-04|
|hJgwshOrnGuOVYSHiQvT| -394148922|1996-09-03|
|RRwPfXMSXfwPTpEbCCYd|-2126030849|2020-11-01|
|NxjZLvalBmUxlHCCdvRS| -868167137|2017-01-09|
|OCKxJFjEWnXFLTnmxlAL|  378510418|2004-09-08|
|FcPQoSKsaWtkVAtsHtmE|-1778979182|1976-06-08|
|gGLrGwLlHQUJgqLoHscd|-1707952693|1975-07-04|
|OQfOJfUAqYMdoDKyIODt| 2042919219|1974-08-18|
+--------------------+-----------+----------+

+--------------------+-----------+----------+
|              string|        int|      date|
+--------------------+-----------+----------+
|YdBiqoUTPchuiVVCToYb|  837577396|2011-10-20|
|ENUTmYcJbIlAHXdXrlcK| 1965683018|1999-06-11|
|qkYABZaLxKSTSKULvJUn|-1534538904|2007-07-21|
|IBekMJxdILbHrseyELjI| -778855686|1995-02-21|
|eOeDuqcyQrmMKyHsdIqi| 2062228449|2021-04-24|
|gvdnhvZEWHxjdVOCNVNO|  634606029|1988-07-28|
|XPooEkKLCsdDBBDPBxdw| 1147520365|2010-10-26|
|QuyvBSnhmNDFViNtZloD| -615531044|1988-11-11|
|wfNVuyjNwLOlIMILwEyY|    -438993|1998-05-08|
|vGqmOojchnEBiFUrIyEF|-1961143065|1995-10-13|
+--------------------+-----------+----------+
.
.
.
```

You can also make use of the `seed` parameter to always get the same results, could be beneficial in some test cases.

And, more importantly, you can make use of the `config` parameter to make sure the fake data in the DataFrames is as close 
to the actual data you use.

For instance, the following:

```python
schema: StructType = StructType([
    StructField("bank_account_number", StringType(), True),
    StructField("string", StringType(), True)
])

config: dict = {
    "string": {
        "data_type": StringType(),
        "provider": "random_element",
        "kwargs": {
            "elements": ('x', 'y')
        },
    },
    "bank_account_number": {
        "data_type": StringType(),
        "provider": "iban",
    }
}

df_gen: DataFrameGenerator = DataFrameGenerator(schema=schema, config=config)
for df in df_gen.arbitrary_dataframes():
    df.show(truncate=False)
```

will result in:

```shell
+----------------------+------+
|bank_account_number   |string|
+----------------------+------+
|GB05ZPOQ53062662223126|x     |
|GB30FBEP02205427369768|y     |
|GB77ZVZD72401097292467|y     |
|GB37ZAUF42921111575037|x     |
|GB94YOYW99106454150303|x     |
|GB45AHZD58341571053644|y     |
|GB49NIWO23000421077097|y     |
|GB57KKMR90126850543238|x     |
|GB36MJSE75788716032200|y     |
|GB09WQRG06056962875254|x     |
+----------------------+------+

+----------------------+------+
|bank_account_number   |string|
+----------------------+------+
|GB05DOHQ75315263055315|x     |
|GB97WKAZ86167865050998|x     |
|GB74FNSZ74818713531062|y     |
|GB09RNUK49954795362800|x     |
|GB52EKEI43974684705487|y     |
|GB71CMIO65098526908411|y     |
|GB21FRNR40256327200553|y     |
|GB78TPWY70848987416423|x     |
|GB72FOTB13893525853918|x     |
|GB88ZPWG41923933222632|y     |
+----------------------+------+
.
.
.
```

The other useful functionality of the DataFrameGenerator is that it can have a transformer function applied to the DataFrames,
perhaps you have a certain transformation that you would like to run over your DataFrame, if so you can pass this function to
the DataFrameGenerator, and it will then run it over the DataFrames and the iterator returned from the `arbitrary_dataframes`
method will now be DataFrames with that transformation applied.

For instance, the following:

```python
schema: StructType = StructType([
    StructField("string", StringType(), True),
    StructField("number1", IntegerType(), True),
    StructField("number2", IntegerType(), True),
])

def transformation(df: DataFrame) -> DataFrame:
    return df.withColumn("number_sum", col("number1") + col("number2")).limit(2)

df_gen: DataFrameGenerator = DataFrameGenerator(schema=schema, transformer=transformation)
for df in df_gen.arbitrary_dataframes():
    df.show(truncate=False)
```

of course, a simple transformation can be in lambda form as well:

```python
df_gen: DataFrameGenerator = DataFrameGenerator(schema=schema, transformer=lambda df: df.withColumn("number_sum", col("number1") + col("number2")).limit(2))
```

will result in:

```shell
+--------------------+-----------+----------+----------+
|string              |number1    |number2   |number_sum|
+--------------------+-----------+----------+----------+
|hfvXIxpHYWmeozQCgDdb|-404644089 |1391745093|987101004 |
|JMeuXcnlUBMabyYkckdL|-1019120536|1893116782|873996246 |
+--------------------+-----------+----------+----------+

+--------------------+-----------+-----------+----------+
|string              |number1    |number2    |number_sum|
+--------------------+-----------+-----------+----------+
|IuGgFufcEWilkamohglP|-1867212230|-1935661407|492093659 |
|rhsttgaKKcWcMVRCSGIk|1412079017 |16007381   |1428086398|
+--------------------+-----------+-----------+----------+

+--------------------+-----------+-----------+-----------+
|string              |number1    |number2    |number_sum |
+--------------------+-----------+-----------+-----------+
|RmihqKGAtoNxmofMNLms|-1729443426|377528902  |-1351914524|
|ZFScHJstlfOpJlvFFKmT|-2142767718|-1554653988|597545590  |
+--------------------+-----------+-----------+-----------+
.
.
.
```

## Property Based Testing Approach

Although far from mature, the code here is a good starting point and hopefully can only be made better, this approach
takes inspiration from the work done by [Holden Karau](https://github.com/holdenk) in the [spark-testing-base](https://github.com/holdenk/spark-testing-base) repository.
You can check the wiki for that [DataFrameGenerator](https://github.com/holdenk/spark-testing-base/wiki/DataFrameGenerator) and see how the scala solution is done there.
Here the approach to property based testing is similar.

There are two methods in the dataframe_generator module, `for_all` and `check_property` that you can make use of to do property checks.

For instance, the following simple test:

```python
def test_that_passes(self):
    schema: StructType = StructType([
        StructField("string", StringType(), True),
        StructField("number1", IntegerType(), True),
        StructField("number2", IntegerType(), True),
    ])

    def transformation(df: DataFrame) -> DataFrame:
        return df.withColumn("number_sum", col("number1") + col("number2")).limit(2)

    df_gen: DataFrameGenerator = DataFrameGenerator(schema=schema, transformer=transformation)

    new_data_schema: StructType = StructType([
        StructField("string", StringType(), True),
        StructField("number1", IntegerType(), True),
        StructField("number2", IntegerType(), True),
        StructField("number_sum", IntegerType(), True),
    ])

    property_results: Iterator[PropertyResult] = for_all(
        dfs=df_gen.arbitrary_dataframes(),
        property_to_check=lambda df: df.schema == new_data_schema and df.count() == 2
    )
    self.assertTrue(check_property(property_results=property_results))
```

will check the property defined in the `property_to_check` parameter in all the DataFrames and generate a report that is
then passed to the `check_property` that will either return True if all DataFrames conform to the property or it will raise
a `PropertyCheckException` and show the failed DataFrames in a pretty table.

Changing the property to check to:

```python
lambda df: df.schema == new_data_schema and df.count() == 3
```

Will cause the test to fail, and it will print out the DataFrames that failed the property check:


```shell
E           chispa.dataframe_generator.PropertyCheckException: Property Check failed:
E           +----------------------+------------+-------------+------------+
E           |        string        |  number1   |   number2   | number_sum |
E           +----------------------+------------+-------------+------------+
E           | eRNTppUYCUECmgCEDLUu | 1035096828 | -1427731638 | -392634810 |
E           | rQPPNXQuSGVuidEnWCxS | 774843839  | -1050333669 | -275489830 |
E           +----------------------+------------+-------------+------------+
E           +----------------------+-------------+-------------+-------------+
E           |        string        |   number1   |   number2   |  number_sum |
E           +----------------------+-------------+-------------+-------------+
E           | DYldTLJOXDsoLmpaSAUQ | -2040281200 |  -106962224 | -2147243424 |
E           | AjSnLZSGoGAjPcufpUgc |  709943750  | -1092598909 |  -382655159 |
E           +----------------------+-------------+-------------+-------------+
E           +----------------------+------------+------------+-------------+
E           |        string        |  number1   |  number2   |  number_sum |
E           +----------------------+------------+------------+-------------+
E           | BStGdFtsgZEyNSdAkLPr | 1526463691 | 1333610860 | -1434892745 |
E           | ddIYTJHNDWSXglhaTrnn | 482503049  | 1506843170 |  1989346219 |
E           +----------------------+------------+------------+-------------+
.
.
.
```

## License

MIT License

Copyright (c) [2022] [Gonçalo André Carneiro de Castro]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
