FROM apache/superset:4.1.1
USER root
RUN pip install duckdb==1.5.4 duckdb-engine==0.15.0
RUN python -c "import duckdb; c=duckdb.connect(); c.execute('INSTALL httpfs'); c.execute('INSTALL iceberg')"
USER superset
