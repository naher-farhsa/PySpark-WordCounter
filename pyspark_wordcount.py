# -*- coding: utf-8 -*-
"""PySpark-WordCount.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1D1pV1HOWc8Fxp6YKv8vbx_hI02sBJidy

#Hello, This project is to demonstrate Apache Spark mapreduce for wordcount and text processing using inbuilt libs and function of Python3.
###1. PySpark
###2. findspark
###3. nltk
###By 6CIT-3:
###1. Rehan Ashraf
###2. Abdul Aman Khan
###3. Mihir Suman
###4. Amal V
###5. Burhan Pasha

###Installing PySpark ( Api for Apache Spark )
"""

# Commented out IPython magic to ensure Python compatibility.
#   %pip install pyspark

"""###Installing findspark library
 To init, config Apache Spark for local python environment
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install findspark
import findspark
findspark.init()

"""##### Importing SparkSession and SparkConf RDDs(Resileint Distributed Dataset)
Creating a SparkContext.
"""

from pyspark.sql import SparkSession
from pyspark.conf import SparkConf

"""
#### Since we write local [*] in the master, it will use all cores in our machine. If we said local [4] it will work with 4 cores. It can work in local / yarn / mesos and kubernetes mode.

#### getOrCreate is used to create a SparkSession if not present.
"""

spark=SparkSession.builder\
    .master("local[*]")\
    .appName("WordCount")\
    .getOrCreate()

"""###SparkContext will create the RDD from txt file"""

sc=spark.sparkContext

"""### Read Datafile - romeojuliet.txt file for wordcount"""

file="/content/romeojuliet.txt"

"""###Read 'file' into rdd 'shakespeare_rdd' and display first 100 lines."""

shakespeare_rdd=sc.textFile(file)

shakespeare_rdd.take(100)

"""###To display number of lines in txt file"""

shakespeare_rdd.count()

"""###Cleaning RDD dateset for any redundancy

###Defining function 'low_clean_str' for converting lines to lowercase and exclude punctuation marks

#### Remove Punctuation and Transform All Words to Lowercase.

#### To exclude all punctuation marks  and convert all words to lowercase, we wrote a function like the one below.
"""

def lower_clean_str(x):
  punc='!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~-'
  lowercased_str = x.lower()
  for ch in punc:
    lowercased_str = lowercased_str.replace(ch, '')
  return lowercased_str

shakespeare_rdd = shakespeare_rdd.map(lower_clean_str)

shakespeare_rdd.take(40)

"""### Using split function to separate the words in all lines ."""

shakespeare_rdd=shakespeare_rdd.flatMap(lambda satir: satir.split(" "))

shakespeare_rdd.take(5)

"""###Using filter function 'filter()' to filter out whitespaces from the RDD dataset ."""

shakespeare_rdd = shakespeare_rdd.filter(lambda x:x!='')

shakespeare_rdd.take(4)

"""### Count how many times each word occurs.
#### To make this calculation we can apply the 'reduceByKey' fucnction to transform as a (key,val) pair for RDD. Hence, first to convert “shakespeare_rdd” to (key,val) pair RDD.

#### In this new (key,val) pair RDD (shakespeare_count), key is the word and val is 1 for each word in RDD (1 represents the number for the each word in “shakespeare_rdd”).

"""

shakespeare_count=shakespeare_rdd.map(lambda  word:(word,1))

shakespeare_count.take(100)

"""###Using 'reducebykey'function to find frequent words in the dataset."""

shakespeare_count_RBK=shakespeare_count.reduceByKey(lambda x,y:(x+y)).sortByKey()

shakespeare_count_RBK.take(40)

"""####Sorting the most frequent words in descending order. As the first step, we switch (key,val) pairs as (val,key)."""

shakespeare_count_RBK=shakespeare_count_RBK.map(lambda x:(x[1],x[0]))

shakespeare_count_RBK.take(30)

"""###The most common word is "the". However, these values are like stopwords which brings values to our analysis."""

shakespeare_count_RBK.sortByKey(False).take(10)

"""###Importing nltk lib to exclude  stopwords words,  and get the list of English stopwords.
####The 'nltk' (Natural Language Toolkit) is used for natural language processing.
"""

import nltk

nltk.download('stopwords')

from nltk.corpus import stopwords
stopwords =stopwords.words('english')
stopwords

"""###After excluding stopwords, the most common word is"romeo"."""

shakespeare_count_RBK = shakespeare_count_RBK.filter(lambda x: x[1] not in stopwords).sortByKey(False)

shakespeare_count_RBK.sortByKey(False).take(50)

"""###Thank You!!
 😄😄
"""

