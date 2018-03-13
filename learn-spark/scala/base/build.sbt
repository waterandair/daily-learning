name := "base"

version := "0.1"

scalaVersion := "2.11.8"

libraryDependencies += "org.apache.spark" %% "spark-core" % "2.2.1"

libraryDependencies += "org.apache.spark" %% "spark-sql" % "2.2.1"

libraryDependencies += "org.apache.spark" %% "spark-streaming" % "2.2.1"

libraryDependencies += "org.apache.spark" %% "spark-streaming-kafka" % "1.6.3"

libraryDependencies += "org.apache.spark" %% "spark-streaming-flume" % "2.2.1"

libraryDependencies += "org.apache.spark" %% "spark-streaming-flume-sink" % "2.2.1"

libraryDependencies += "org.apache.spark" %% "spark-hive" % "2.2.1"

libraryDependencies += "org.scala-lang" % "scala-library" % "2.11.8"

libraryDependencies += "org.apache.commons" % "commons-lang3" % "3.5"

libraryDependencies += "mysql" % "mysql-connector-java" % "5.1.6"

libraryDependencies += "com.alibaba" % "fastjson" % "1.2.44"

libraryDependencies += "org.scalanlp" % "breeze_2.10" % "0.10"