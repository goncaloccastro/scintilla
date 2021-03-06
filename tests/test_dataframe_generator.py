from dataclasses import replace
from typing import Iterator, List
from unittest import TestCase

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import lit
from pyspark.sql.types import StringType, StructType, StructField, LongType, DateType, ByteType, ShortType, IntegerType, \
    DecimalType, FloatType, DoubleType, BooleanType, BinaryType, TimestampType, ArrayType

from scintilla.dataframe_generator import DataFrameGenerator, for_all, check_property, DataConfig, PropertyResult, \
    PropertyCheckException, \
    DataTypeMissingException


class TestDataFrameGenerator(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.spark = SparkSession.builder.appName("scintilla").getOrCreate()

        cls.schema: StructType = StructType([
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
        cls.df_gen: DataFrameGenerator = DataFrameGenerator(schema=cls.schema, seed=0)

        cls.test_data = ([1, "dick smith"], [2, "jane smith"], [3, "nick smith"])
        cls.test_data_schema: StructType = StructType([
            StructField('id', StringType(), True),
            StructField('name', StringType(), True)
        ])
        cls.test_df: DataFrame = cls.spark.createDataFrame(data=cls.test_data, schema=cls.test_data_schema)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.spark.stop()

    def test_for_all_given_no_dataframe_and_invalid_property_should_return_empty_list(self):
        dfs: Iterator[DataFrame] = iter([])

        actual: List[PropertyResult] = list(for_all(
            dfs=dfs,
            property_to_check=None)
        )
        expected: List[PropertyResult] = []

        self.assertEqual(expected, actual)

    def test_for_all_given_single_dataframe_and_valid_property_should_return_correct_result(self):
        dfs: Iterator[DataFrame] = iter([self.test_df])

        actual: List[PropertyResult] = list(for_all(
            dfs=dfs,
            property_to_check=lambda df: df.schema == self.test_data_schema and df.count() == 3)
        )
        expected: List[PropertyResult] = [PropertyResult(property_check=True, dataframe=self.test_df)]

        self.assertEqual(expected, actual)

    def test_for_all_given_multiple_dataframes_and_valid_property_should_return_correct_result(self):
        dfs: Iterator[DataFrame] = iter([self.test_df, self.test_df])

        actual: List[PropertyResult] = list(for_all(
            dfs=dfs,
            property_to_check=lambda df: df.schema == self.test_data_schema and df.count() == 3)
        )
        expected: List[PropertyResult] = [
            PropertyResult(property_check=True, dataframe=self.test_df),
            PropertyResult(property_check=True, dataframe=self.test_df)
        ]

        self.assertEqual(expected, actual)

    def test_check_property_given_no_result_should_return_true(self):
        results: Iterator[PropertyResult] = iter([])

        actual: bool = check_property(property_results=results)

        self.assertTrue(actual)

    def test_check_property_given_valid_result_should_return_true(self):
        results: Iterator[PropertyResult] = iter([PropertyResult(property_check=True, dataframe=self.test_df)])

        actual: bool = check_property(property_results=results)

        self.assertTrue(actual)

    def test_check_property_given_invalid_results_should_raise_exception(self):
        results: Iterator[PropertyResult] = iter([PropertyResult(property_check=False, dataframe=self.test_df)])

        self.assertRaises(PropertyCheckException, check_property, property_results=results)

    def test_arbitrary_dataframes_should_return_correct_default_values_for_dataframes(self):
        actual: List[DataFrame] = list(self.df_gen.arbitrary_dataframes())
        length_check: bool = len(actual) == self.df_gen.num_dataframes
        number_records_check: bool = all([elem.count() == self.df_gen.num_records for elem in actual])
        schema_check: bool = all([elem.schema == self.schema for elem in actual])

        self.assertTrue(all([length_check, number_records_check, schema_check]))

    def test_arbitrary_dataframes_with_invalid_transformer_should_raise_exception(self):
        df_gen_with_config: DataFrameGenerator = replace(
            self.df_gen,
            transformer=lambda x: x + 1
        )

        self.assertRaises(Exception, df_gen_with_config.arbitrary_dataframes())

    def test_arbitrary_dataframes_with_transformer_should_return_correct_default_values_for_dataframes(self):
        number_of_records: int = 10
        new_column_name: str = "literal"
        df_gen_with_config: DataFrameGenerator = replace(
            self.df_gen,
            transformer=lambda df: df.withColumn(new_column_name, lit(1)).limit(number_of_records)
        )
        schema = StructType([
            StructField("expected_name", StringType(), True),
            StructField("int", IntegerType(), True),
            StructField("long", LongType(), True),
            StructField("byte", ByteType(), True),
            StructField("short", ShortType(), True),
            StructField("double", DoubleType(), True),
            StructField("float", FloatType(), True),
            StructField("decimal", DecimalType(10, 0), True),
            StructField("bool", BooleanType(), True),
            StructField("binary", BinaryType(), True),
            StructField("date", DateType(), True),
            StructField("timestamp", TimestampType(), True),
            StructField(new_column_name, IntegerType(), False)
        ])

        actual: List[DataFrame] = list(df_gen_with_config.arbitrary_dataframes())
        number_records_check: bool = all([elem.count() == number_of_records for elem in actual])
        schema_check: bool = all([elem.schema == schema for elem in actual])

        self.assertTrue(all([number_records_check, schema_check]))

    def test_get_datatype_and_provider_given_schema_field_with_no_expected_type_should_raise_exception(self):
        schema_field: StructField = StructField("expected_name", ArrayType(StringType()), True)

        self.assertRaises(DataTypeMissingException, self.df_gen.get_datatype_and_provider, schema_field=schema_field)

    def test_get_datatype_and_provider_given_a_schema_field_should_return_correct_data_config_object(self):
        schema_field: StructField = StructField("expected_name", StringType(), True)

        actual: DataConfig = self.df_gen.get_datatype_and_provider(schema_field=schema_field)
        expected: DataConfig = DataConfig(data_type="StringType", provider='pystr', kwargs={})

        self.assertEqual(expected, actual)

    def test_get_datatype_and_provider_given_a_schema_field_and_config_should_return_correct_data_config_object(self):
        config: dict = {"expected_name": {
            "data_type": StringType(),
            "provider": "random_element",
            "kwargs": {
                "elements": ('x', 'y')
            }
        }}
        df_gen_with_config: DataFrameGenerator = replace(self.df_gen, config=config)
        schema_field: StructField = StructField("expected_name", StringType(), True)

        actual: DataConfig = df_gen_with_config.get_datatype_and_provider(schema_field=schema_field)
        expected: DataConfig = DataConfig(
            data_type="StringType",
            provider='random_element',
            kwargs={"elements": ('x', 'y')}
        )

        self.assertEqual(expected, actual)

    def test_use_providers_given_data_config_object_should_return_the_correct_value(self):
        data_config: DataConfig = DataConfig(data_type="StringType", provider="pystr")

        actual: str = self.df_gen.use_providers(data_config=data_config)
        expected: str = "RNvnAvOpyEVAoNGnVZQU"

        self.assertEqual(expected, actual)

    def test_use_providers_given_data_config_object_with_provider_and_keyword_arguments_should_return_the_correct_value(
            self):
        data_config: DataConfig = DataConfig(
            data_type="StringType",
            provider="random_element",
            kwargs={
                "elements": ('x', 'y')
            }
        )

        actual: str = self.df_gen.use_providers(data_config=data_config)
        expected: str = "y"

        self.assertEqual(expected, actual)

    def test_generate_data_given_a_known_schema_should_return_correct_dataframe(self):
        actual: DataFrame = self.df_gen.generate_data()
        actual_count: int = actual.count()
        actual_schema: StructType = actual.schema

        expected_count: int = 10
        expected_schema: StructType = self.schema

        self.assertTrue(actual_count == expected_count and actual_schema == expected_schema)
