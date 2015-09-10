# coding: gbk
# +--------------------------------------------------------------------------+
# |  Licensed Materials - Property of IBM                                    |
# |                                                                          |
# | (C) Copyright IBM Corporation 2008.                                      |
# +--------------------------------------------------------------------------+
# | This module complies with SQLAlchemy 0.4 and is                          |
# | Licensed under the Apache License, Version 2.0 (the "License");          |
# | you may not use this file except in compliance with the License.         |
# | You may obtain a copy of the License at                                  |
# | http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable |
# | law or agreed to in writing, software distributed under the License is   |
# | distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY |
# | KIND, either express or implied. See the License for the specific        |
# | language governing permissions and limitations under the License.        |
# +--------------------------------------------------------------------------+
# | Authors: Alex Pitigoi, Abhigyan Agrawal                                                    |
# | Version: 0.1.6                                                           |
# +--------------------------------------------------------------------------+

"""
This module implements the SQLAlchemy version 0.4 for IBM DB2 Data Servers.
"""

from sqlalchemy import sql, engine, schema, exceptions, log
from sqlalchemy import types as sa_types
from sqlalchemy.engine import base, default, url
from sqlalchemy.sql import compiler

import pickle, os.path, re, datetime

# Load IBM_DB reserved words associated with supported IBM Data Servers (DB2)
# ibm_db_reserved is a pickle file expected to share path with current file
RESERVED_WORDS = ['activate', 'disallow', 'locale', 'result', 'add', 'disconnect', 'localtime', 
                  'result_set_locator', 'after', 'distinct', 'localtimestamp', 'return', 'alias', 
                  'do', 'locator', 'returns', 'all', 'double', 'locators', 'revoke', 'allocate', 
                  'drop', 'lock', 'right', 'allow', 'dssize', 'lockmax', 'rollback', 'alter', 
                  'dynamic', 'locksize', 'routine', 'and', 'each', 'long', 'row', 'any', 'editproc', 
                  'loop', 'row_number', 'as', 'else', 'maintained', 'rownumber', 'asensitive', 'elseif', 
                  'materialized', 'rows', 'associate', 'enable', 'maxvalue', 'rowset', 'asutime', 'encoding', 
                  'microsecond', 'rrn', 'at', 'encryption', 'microseconds', 'run', 'attributes', 'end', 'minute', 
                  'savepoint', 'audit', 'end-exec', 'minutes', 'schema', 'authorization', 'ending', 'minvalue', 
                  'scratchpad', 'aux', 'erase', 'mode', 'scroll', 'auxiliary', 'escape', 'modifies', 'search', 
                  'before', 'every', 'month', 'second', 'begin', 'except', 'months', 'seconds', 'between', 'exception', 
                  'new', 'secqty', 'binary', 'excluding', 'new_table', 'security', 'bufferpool', 'exclusive', 'nextval', 
                  'select', 'by', 'execute', 'no', 'sensitive', 'cache', 'exists', 'nocache', 'sequence', 'call', 'exit', 
                  'nocycle', 'session', 'called', 'explain', 'nodename', 'session_user', 'capture', 'external', 
                  'nodenumber', 'set', 'cardinality', 'extract', 'nomaxvalue', 'signal', 'cascaded', 'fenced', 
                  'nominvalue', 'simple', 'case', 'fetch', 'none', 'some', 'cast', 'fieldproc', 'noorder', 
                  'source', 'ccsid', 'file', 'normalized', 'specific', 'char', 'final', 'not', 'sql', 
                  'character', 'for', 'null', 'sqlid', 'check', 'foreign', 'nulls', 'stacked', 'close', 
                  'free', 'numparts', 'standard', 'cluster', 'from', 'obid', 'start', 'collection', 
                  'full', 'of', 'starting', 'collid', 'function', 'old', 'statement', 'column', 'general', 
                  'old_table', 'static', 'comment', 'generated', 'on', 'stay', 'commit', 'get', 'open', 
                  'stogroup', 'concat', 'global', 'optimization', 'stores', 'condition', 'go', 'optimize', 
                  'style', 'connect', 'goto', 'option', 'substring', 'connection', 'grant', 'or', 'summary', 
                  'constraint', 'graphic', 'order', 'synonym', 'contains', 'group', 'out', 'sysfun', 'continue', 
                  'handler', 'outer', 'sysibm', 'count', 'hash', 'over', 'sysproc', 'count_big', 'hashed_value', 
                  'overriding', 'system', 'create', 'having', 'package', 'system_user', 'cross', 'hint', 'padded', 
                  'table', 'current', 'hold', 'pagesize', 'tablespace', 'current_date', 'hour', 'parameter', 'then', 
                  'current_lc_ctype', 'hours', 'part', 'time', 'current_path', 'identity', 'partition', 'timestamp', 
                  'current_schema', 'if','partitioned', 'to', 'current_server', 'immediate', 'partitioning', 
                  'transaction', 'current_time', 'in', 'partitions', 'trigger', 'current_timestamp', 'including', 
                  'password', 'trim', 'current_timezone', 'inclusive', 'path', 'type', 'current_user', 'increment', 
                  'piecesize', 'undo', 'cursor', 'index', 'plan', 'union', 'cycle', 'indicator', 'position', 'unique', 
                  'data', 'inherit', 'precision', 'until', 'database', 'inner', 'prepare', 'update', 'datapartitionname', 
                  'inout', 'prevval', 'usage', 'datapartitionnum', 'insensitive', 'primary', 'user', 'date', 'insert', 
                  'priqty', 'using', 'day', 'integrity', 'privileges', 'validproc', 'days', 'intersect', 'procedure', 
                  'value', 'db2general', 'into', 'program', 'values', 'db2genrl', 'is', 'psid', 'variable', 'db2sql', 
                  'isobid', 'query', 'variant', 'dbinfo', 'isolation', 'queryno', 'vcat', 'dbpartitionname', 'iterate', 
                  'range', 'version', 'dbpartitionnum', 'jar', 'rank', 'view', 'deallocate', 'java', 'read', 'volatile', 
                  'declare', 'join', 'reads', 'volumes', 'default', 'key', 'recovery', 'when', 'defaults', 'label', 
                  'references', 'whenever', 'definition', 'language', 'referencing', 'where', 'delete', 'lateral', 
                  'refresh', 'while', 'dense_rank', 'lc_ctype', 'release', 'with', 'denserank', 'leave', 'rename', 
                  'without', 'describe', 'left', 'repeat', 'wlm', 'descriptor', 'like', 'reset', 'write', 'deterministic', 
                  'linktype', 'resignal', 'xmlelement', 'diagnostics', 'local', 'restart', 'year', 'disable', 'localdate', 
                  'restrict', 'years', 'abs', 'grouping', 'regr_intercept', 'are', 'int', 'regr_r2', 'array', 'integer', 
                  'regr_slope', 'asymmetric', 'intersection', 'regr_sxx', 'atomic', 'interval', 'regr_sxy', 'avg', 'large', 
                  'regr_syy', 'bigint', 'leading', 'rollup', 'blob', 'ln', 'scope', 'boolean', 'lower', 'similar', 'both', 
                  'match', 'smallint', 'ceil', 'max', 'specifictype', 'ceiling', 'member', 'sqlexception', 'char_length', 
                  'merge', 'sqlstate', 'character_length', 'method', 'sqlwarning', 'clob', 'min', 'sqrt', 'coalesce', 'mod', 
                  'stddev_pop', 'collate', 'module', 'stddev_samp', 'collect', 'multiset', 'submultiset', 'convert', 'national', 
                  'sum', 'corr', 'natural', 'symmetric', 'corresponding', 'nchar', 'tablesample', 'covar_pop', 'nclob', 
                  'timezone_hour', 'covar_samp', 'normalize', 'timezone_minute', 'cube', 'nullif', 'trailing', 'cume_dist', 
                  'numeric', 'translate', 'current_default_transform_group', 'octet_length', 'translation', 'current_role', 
                  'only', 'treat', 'current_transform_group_for_type', 'overlaps', 'true', 'dec', 'overlay', 'uescape', 'decimal', 
                  'percent_rank', 'unknown', 'deref', 'percentile_cont', 'unnest', 'element', 'percentile_disc', 'upper', 'exec', 
                  'power', 'var_pop', 'exp', 'real', 'var_samp', 'false', 'recursive', 'varchar', 'filter', 'ref', 'varying', 
                  'float', 'regr_avgx', 'width_bucket', 'floor', 'regr_avgy', 'window', 'fusion', 'regr_count', 'within']

# Override module sqlalchemy.types
class IBM_DBBinary(sa_types.Binary):
  def get_col_spec(self):
    if self.length is None:
      return "BLOB(1M)"
    else:
      return "BLOB(%s)" % self.length

class IBM_DBString(sa_types.String):
  def get_col_spec(self):
    if self.length is None:
      return "LONG VARCHAR"
    else:
      return "VARCHAR(%s)" % self.length
      
class IBM_DBBoolean(sa_types.Boolean):
  def get_col_spec(self):
    return "SMALLINT"

  def result_processor(self, dialect):
    def process(value):
      if value is None:
        return None
      if value == False:
        return 0
      elif value == True:
        return 1
    return process

  def bind_processor(self, dialect):
    def process(value):
      if value is None:
        return None
      if value == False:
        return '0'
      elif value == True:
        return '1'
    return process    

class IBM_DBInteger(sa_types.Integer):
  def get_col_spec(self):
    return "INTEGER"

class IBM_DBNumeric(sa_types.Numeric):
  def get_col_spec(self):
    if not self.precision:
      return "DECIMAL(31,0)"
    else:
      return "DECIMAL(%(precision)s, %(length)s)" % {'precision': self.precision, 'length' : self.scale}

class IBM_DBDateTime(sa_types.DateTime):
  def get_col_spec(self):
    return "TIMESTAMP"

  def result_processor(self, dialect):
    def process(value):
      if value is None:
        return None
      if isinstance(value, datetime.datetime):
          value = datetime.datetime( value.year, value.month, value.day,
                                     value.hour, value.minute, value.second, value.microsecond)
      elif isinstance(value, datetime.time):
          value = datetime.datetime( value.year, value.month, value.day, 0, 0, 0, 0)
      return value
    return process

  def bind_processor(self, dialect):
    def process(value):
      if value is None:
        return None
      if isinstance(value, datetime.datetime):
          value = datetime.datetime( value.year, value.month, value.day,
                                     value.hour, value.minute, value.second, value.microsecond)
      elif isinstance(value, datetime.date):
          value = datetime.datetime( value.year, value.month, value.day, 0, 0, 0, 0)
      return str(value)
    return process

class IBM_DBDate(sa_types.Date):

  def get_col_spec(self):
    return "DATE"

  def result_processor(self, dialect):
    def process(value):
      if value is None:
        return None
      if isinstance(value, datetime.datetime):
          value = datetime.date( value.year, value.month, value.day)
      elif isinstance(value, datetime.date):
          value = datetime.date( value.year, value.month, value.day)
      return value
    return process

  def bind_processor(self, dialect):
    def process(value):
      if value is None:
        return None
      if isinstance(value, datetime.datetime):
          value = datetime.date( value.year, value.month, value.day)
      elif isinstance(value, datetime.time):
          value = datetime.date( value.year, value.month, value.day)
      return str(value)
    return process

class IBM_DBTime(sa_types.Time):
  def get_col_spec(self):
    return 'TIME'

class IBM_DBTimeStamp(sa_types.TIMESTAMP):
  def get_col_spec(self):
    return 'TIMESTAMP'

class IBM_DBDATETIME(sa_types.DATETIME):
  def get_col_spec(self):
    return 'TIMESTAMP'

class IBM_DBSmallInteger(sa_types.SmallInteger):
  def get_col_spec(self):
    return 'SMALLINT'

class IBM_DBFloat(sa_types.Float):
  def get_col_spec(self):
    return 'REAL'

class IBM_DBFLOAT(sa_types.FLOAT):
  def get_col_spec(self):
    return 'REAL'

class IBM_DBTEXT(sa_types.TEXT):
  def get_col_spec(self):
    if self.length is None:
      return 'LONG VARCHAR'
    else:
      return 'VARCHAR(%s)' % self.length
    
class IBM_DBDecimal(sa_types.DECIMAL):
  def get_col_spec(self):
    if not self.precision:
      return 'DECIMAL(31,0)'
    else:
      return 'DECIMAL(%(precision)s, %(length)s)' % {'precision': self.precision, 'length' : self.length}

class IBM_DBINT(sa_types.INT):
  def get_col_spec(self):
    return 'INT'

class IBM_DBCLOB(sa_types.CLOB):
  def get_col_spec(self):
    return 'CLOB'

class IBM_DBVARCHAR(sa_types.VARCHAR):
  def get_col_spec(self):
    if self.length is None:
      return 'LONG VARCHAR'
    else:
      return 'VARCHAR(%s)' % self.length

class IBM_DBChar(sa_types.CHAR):
  def get_col_spec(self):
    if self.length is None:
      return 'CHAR'
    else:
      return 'CHAR(%s)' % self.length
      
class IBM_DBBLOB(sa_types.BLOB):
  def get_col_spec(self):
    if self.length is None:
      return 'BLOB(1M)'
    else:
      return 'BLOB(%s)' % self.length

class IBM_DBBOOLEAN(sa_types.BOOLEAN):
  def get_col_spec(self):
    return 'SMALLINT'

class IBM_DBDouble(sa_types.Float):
  def get_col_spec(self):
    if self.length is None:
      return 'DOUBLE(15)'
    else:
      return 'DOUBLE(%(precision)s)' % self.precision

class IBM_DBBigInteger(sa_types.TypeEngine):
  def get_col_spec(self):
    return 'BIGINT'

class IBM_DBXML(sa_types.TypeEngine):
  def get_col_spec(self):
    return 'XML'


# Module level dictionary maps standard SQLAlchemy types to IBM_DB data types.
# The dictionary uses the SQLAlchemy data types as key, and maps an IBM_DB type as its value 
colspecs = {
    sa_types.Binary       : IBM_DBBinary,
    sa_types.String       : IBM_DBString,
    sa_types.Boolean      : IBM_DBBoolean,
    sa_types.Integer      : IBM_DBInteger,
    sa_types.Numeric      : IBM_DBNumeric,
    sa_types.DateTime     : IBM_DBDateTime,
    sa_types.Date         : IBM_DBDate,
    sa_types.Time         : IBM_DBTime,
    sa_types.SmallInteger : IBM_DBSmallInteger,
    sa_types.Float        : IBM_DBFloat,
    sa_types.FLOAT        : IBM_DBFloat,
    sa_types.TEXT         : IBM_DBTEXT,
    sa_types.DECIMAL      : IBM_DBDecimal,
    sa_types.INT          : IBM_DBINT,
    sa_types.TIMESTAMP    : IBM_DBTimeStamp,
    sa_types.DATETIME     : IBM_DBDATETIME,
    sa_types.CLOB         : IBM_DBCLOB,
    sa_types.VARCHAR      : IBM_DBVARCHAR,
    sa_types.CHAR         : IBM_DBChar,
    sa_types.BLOB         : IBM_DBBLOB,
    sa_types.BOOLEAN      : IBM_DBBOOLEAN
}

# Module level dictionary which maps the data type name returned by a database
# to the IBM_DB type class allowing the correct type classes to be created 
# based on the information_schema.  Any database type that is supported by the 
# IBM_DB shall be mapped to an equivalent data type.
ischema_names = {
    'BLOB'         : IBM_DBBinary,
    'BINARY LARGE OBJECT'         : IBM_DBBinary,
    'CHAR'         : IBM_DBChar,
    'CHARACTER'         : IBM_DBChar,
    'CLOB'         : IBM_DBCLOB,
    'CHARACTER LARGE OBJECT'         : IBM_DBCLOB,
    'DATE'         : IBM_DBDate,
    'DATETIME'     : IBM_DBDateTime,
    'INTEGER'      : IBM_DBInteger,
    'SMALLINT'     : IBM_DBSmallInteger,
    'BIGINT'       : IBM_DBBigInteger,
    'DECIMAL'      : IBM_DBDecimal,
    'REAL'         : IBM_DBFloat,
    'DOUBLE'       : IBM_DBDouble,
    'DOUBLE PRECISION'       : IBM_DBDouble,
    'TIME'         : IBM_DBTime,
    'TIMESTAMP'    : IBM_DBTimeStamp,
    'VARCHAR'      : IBM_DBString,
    'CHARACTER VARYING' : IBM_DBString,
    'LONG VARCHAR' : IBM_DBTEXT,
    'XML'          : IBM_DBXML
}


# Define the behavior of a specific database and DBAPI combination.
# Its main responsibility is to act as interface between SQLAlchemy and the DBAPI driver.
# Aspects that are specific to the data server are defined in this class including, 
# but not limited to, metadata definition, SQL-syntax for use in SQL query generation, 
# execution, and result-set handling.
class IBM_DBDialect(default.DefaultDialect):
  positional                   = True
  encoding                     = 'gbk'
  max_identifier_length        = 128
  supports_alter               = True
  supports_sane_rowcount       = True
  supports_sane_multi_rowcount = True
  preexecute_sequences         = False
  supports_unicode_statements  = False
  name = 'db2'
  
  def __init__(self, **kwargs):
    """ Inputs: Supports any number of keyword arguments. 
                Attributes not set by default or not set by the dialect module level 
                class should be set here.
    """
    default.DefaultDialect.__init__(self, **kwargs)

    """String constant for parameter marker formatting expected.
       Possible values {'qmark', 'numeric', 'named', 'format', 'pyformat'}
       associated with { name=?,  name=:1,   :name,    %s,     %(name)s  }
    """
    self.paramstyle = IBM_DBDialect.dbapi().paramstyle


  # Returns the underlying DBAPI driver module for access to class attributes/variables
  def dbapi(cls):
    """ Returns: the underlying DBAPI driver module
    """
    import DB2 as module
    return module
  dbapi = classmethod(dbapi)


  # Retrieves the IBM Data Server version for a given connection object
  def server_version_info(self, connection):
    """ Inputs: - sqlalchemy.engine.base.Connection object has a <connection> reference
                  to sqlalchemy.pool._ConnectionFairy which has a <connection> reference
                  to sqlalchemy.databases.ibm_db_dbi.Connection, the actual DBAPI
                  driver connection handler:
                      sa_connection   = connection
                      sa_conn_fairy   = sa_connection.connection
                      ibm_db_dbi_conn = sa_conn_fairy.connection
        Returns: Tuple, representing the data server version.
    """
    version_info = connection.connection.connection.server_info()
    return version_info


  # Build DB-API compatible connection arguments.
  def create_connect_args(self, url):
    """ Inputs:  sqlalchemy.engine.url object (attributes parsed from a RFC-1738-style string using
                 module-level make_url() function - driver://username:password@host:port/database or
                 driver:///?<attrib_1_name>=<attrib_1_value>;<attrib_2_name>=<attrib_2_value>)
        Returns: tuple consisting of a *args/**kwargs suitable to send directly to the dbapi connect function.
                 DBAPI.connect(dsn, user='', password='', host='', database='', conn_options=None)
                 DSN: 'DRIVER={IBM DB2 ODBC DRIVER};DATABASE=db_name;HOSTNAME=host_addr;
                       PORT=50000;PROTOCOL=TCPIP;UID=user_id;PWD=secret'
    """
    conn_args = url.translate_connect_args()

    # DSN support through CLI configuration (../cfg/db2cli.ini), while 2 connection
    # attributes are mandatory: database alias and UID (in support to current schema),
    # all the other connection attributes (protocol, hostname, servicename) are provided
    # through db2cli.ini database catalog entry.
    # Example 1: ibm_db_sa:///<database_alias>?UID=db2inst1 or 
    # Example 2: ibm_db_sa:///?DSN=<database_alias>;UID=db2inst1
    if str(url).find('///') != -1:
      dsn, uid, pwd = '', '', ''
      if 'database' in conn_args and conn_args['database'] is not None:
        dsn = conn_args['database']
      else:
        if 'DSN' in url.query and url.query['DSN'] is not None:
          dsn = url.query['DSN']
      if 'UID' in url.query and url.query['UID'] is not None:
        uid = url.query['UID']
      if 'PWD' in url.query and url.query['PWD'] is not None:
        pwd = url.query['PWD']
      return ((dsn, uid, pwd,'',''), {})
    else:
      # Full URL string support for connection to remote data servers
      return ( () , { 'dsn':conn_args['database'] , 'uid':conn_args['username'] , 'pwd':conn_args['password'] } )
      #return ((dsn, conn_args['username'],'','',''), {})

  # Builds an execution context
  def create_execution_context(self,
                               connection,
                               compiled = None,
                               compiled_parameters = None,
                               statement = None,
                               parameters = None):
    """ Inputs: Use the supplied parameters to construct a new ExecutionContext.
                The parameters should be passed on directly to the ExectionContext 
                constructor, which knows how to use them to build the execution context.
                Connection object which is a proxy object to a DBAPI driver connection
        Returns: ExecutionContext object
    """
    dialect.logger.debug("\n  ***  IBM_DBDialect::create_execution_context: " + str(statement))
    return IBM_DBExecutionContext( self, connection, compiled, statement, parameters )


  # Retrieves current schema for the specified connection object
  def get_default_schema_name(self, connection):
    """ Inputs: - sqlalchemy.engine.base.Connection object has a <connection> reference
                  to sqlalchemy.pool._ConnectionFairy which has a <connection> reference
                  to sqlalchemy.databases.ibm_db_dbi.Connection, the actual DBAPI
                  driver connection handler
        Returns: representing the current schema.
    """
    cu = connection.connection.connection.cursor()
    cu.execute( "select CURRENT schema from sysibm.sysdummy1" )
    r = cu.fetchone()
    return r[0]

  # Verifies if a specific table exists for a given schema
  def has_table(self, connection, table_name, schema=None):
    """ Inputs: - sqlalchemy.engine.base.Connection object has a <connection> reference
                  to sqlalchemy.pool._ConnectionFairy which has a <connection> reference
                  to sqlalchemy.databases.ibm_db_dbi.Connection, the actual DBAPI
                  driver connection handler
                - table_name string
                - schema string, if not using the default schema
        Returns: True, if table exsits, False otherwise.
    """
    if schema is None:
        schema = self.get_default_schema_name(connection)
    #table = connection.connection.connection.tables(schema, table_name)
    cu = connection.connection.connection.cursor()
    cu.execute( "select TABLE_NAME from SYSIBM.TABLES where TABLE_SCHEMA = '%s' and TABLE_TYPE = 'BASE TABLE' and TABLE_NAME='%s'" % ( schema.upper() , table_name.upper() ) )
    table = [ x[0] for x in cu.fetchall() ]
    has_it = table is not None and \
             len(table) is not 0 \
             and table[0] == table_name.upper()
    dialect.logger.debug("\n  ***  IBM_DBDialect::has_table( "+str(table_name)+', '+str(schema)+' ) = '+str(has_it))
    return has_it

  # Retrieves a list of table names for a given schema
  def table_names(self, connection, schema = None):
    """ Inputs: - sqlalchemy.engine.base.Connection object has a <connection> reference
                  to sqlalchemy.pool._ConnectionFairy which has a <connection> reference
                  to sqlalchemy.databases.ibm_db_dbi.Connection, the actual DBAPI
                  driver connection handler
                - schema string, if not using the default schema
        Returns: List of strings representing table names
    """
    if schema is None:
        schema = self.get_default_schema_name(connection)
    names = []
    #tables = connection.connection.connection.tables(schema)
    cu = connection.connection.connection.cursor()
    cu.execute( "select TABLE_NAME from SYSIBM.TABLES where TABLE_SCHEMA = '%s' and TABLE_TYPE = 'BASE TABLE'" % schema.upper() )
    tables = [ x[0] for x in cu.fetchall() ]
    for table in tables:
      names.append(table['TABLE_NAME'].lower())
    dialect.logger.debug("\n  ***  IBM_DBDialect::table_names: " + str(names))
    return names


  # Retrieves a list of index names for a given schema
  def index_names(self, connection, table_name, schema = None):
    dialect.logger.debug("\n  ***  IBM_DBDialect::index_names( "+str(table_name)+', '+str(schema)+' )')
    """ Inputs: - sqlalchemy.engine.base.Connection object has a <connection> reference
                  to sqlalchemy.pool._ConnectionFairy which has a <connection> reference
                  to sqlalchemy.databases.ibm_db_dbi.Connection, the actual DBAPI
                  driver connection handler
                - table_name string
                - schema string, if not using the default schema
        Returns: List of strings representing table names
    """
    if schema is None:
        schema = self.get_default_schema_name(connection)

    names = []
    index = connection.connection.connection.index(schema)
    return index


  # Loads table description (columns and properties) from the database for a given table object
  def reflecttable(self, connection, table, include_columns = None):
    """ Inputs: - sqlalchemy.engine.base.Connection object has a <connection> reference
                  to sqlalchemy.pool._ConnectionFairy which has a <connection> reference
                  to sqlalchemy.databases.ibm_db_dbi.Connection, the actual DBAPI
                  driver connection handler
                - table object
                - include_columns (a list or set) limits the autoload to the given column names.
    """
    dialect.logger.debug("\n  ***  IBM_DBDialect::reflecttable( "+str(table)+', '+str(include_columns)+' )')
    ibm_dbi_conn = connection.connection.connection
    schema_name = self.get_default_schema_name(connection)
    if table.schema is not None:
        schema_name = table.schema

    # Append columns to table
    #columns = ibm_dbi_conn.columns( schema_name, table.name, include_columns)
    cu = ibm_dbi_conn.cursor()
    cu.execute( """select TABLE_NAME , COLUMN_NAME , ORDINAL_POSITION , DATA_TYPE as TYPE_NAME , IS_NULLABLE 
                    from SYSIBM.COLUMNS where TABLE_SCHEMA = '%s' and TABLE_NAME = '%s'""" % ( schema_name.upper() , table.name.upper() ) )
    columns = cu.fetchall()
    
    if not columns:
      raise exceptions.NoSuchTableError(table.name)

    for col in columns:
      (tab_name, col_name, col_id, col_type, is_nullable) = (
        col[0].lower(),
        col[1].lower(),
        col[2],
        col[3],
        col[4] == 'YES' )
      col_args= []
      type = ischema_names.get(col_type, None)
      column = schema.Column(col_name, type, nullable=is_nullable, *col_args)
      dialect.logger.debug("\n  ***  column: " + repr(column))
      table.append_column(column)

    # Define table's primary keys
    # 由于用处不大，暂时不处理
    """
    pkeys = ibm_dbi_conn.primary_keys( True, schema_name, table.name)
    for pkey in pkeys:
      (pk_schema, pk_table, pk_column, pk_name, key_seq) = (
        pkey['TABLE_SCHEM'].lower(),
        pkey['TABLE_NAME'].lower(),
        pkey['COLUMN_NAME'].lower(),
        pkey['PK_NAME'].lower(),
        pkey['KEY_SEQ']
      )
      table.primary_key.add(table.c[pk_column])

    # Define table's other indexes
    indexes = ibm_dbi_conn.indexes( True, schema_name, table.name)
    for idx in indexes:
      (idx_schema, idx_table, idx_col, idx_name, idx_id, idx_type, is_unique, ascendent) = (
        idx['TABLE_SCHEM'].lower(),
        idx['TABLE_NAME'].lower(),
        idx['COLUMN_NAME'].lower(),
        idx['INDEX_NAME'].lower(),
        idx['ORDINAL_POSITION'],
        idx['TYPE'],
        idx['NON_UNIQUE']  == 0,
        idx['ASC_OR_DESC'] == 'A'
      )
      dialect.logger.debug("\n  ***  IBM_DBDialect::reflecttable: indexes: " + str(idx))

    # Define table's foreign keys
    fkeys = ibm_dbi_conn.foreign_keys( True, schema_name, table.name)
    for fkey in fkeys:
      ( pk_schema, pk_table, pk_column, pk_name, key_seq, 
        fk_schema, fk_table, fk_column, fk_name) = (
        fkey['PKTABLE_SCHEM'].lower(),
        fkey['PKTABLE_NAME'].lower(),
        fkey['PKCOLUMN_NAME'].lower(),
        fkey['PK_NAME'].lower(),
        fkey['KEY_SEQ'],
        fkey['FKTABLE_SCHEM'].lower(),
        fkey['FKTABLE_NAME'].lower(),
        fkey['FKCOLUMN_NAME'].lower(),
        fkey['FK_NAME'].lower()
      )
      table.append_constraint(schema.ForeignKeyConstraint( ['%s'%(fk_column)],
                                                           ['%s.%s'%(pk_table,pk_column)]))
    dialect.logger.debug("\n  ***  IBM_DBDialect::reflecttable: table: " + repr(table))
    """

  # Checks if the DB_API driver error indicates an invalid connection
  def is_disconnect(self, ex):
    """ Inputs: DB_API driver exception to be checked for invalid connection
        Returns: True, if the exception indicates invalid connection, False otherwise.
    """
    if isinstance(ex, (self.dbapi.ProgrammingError,
                       self.dbapi.OperationalError)):
        is_closed = 'Connection is not active' in str(ex) or \
                    'connection is no longer active' in str(ex) or \
                    'Connection Resource cannot be found' in str(ex)
        return is_closed
    else:
        return False


  # Returns the OID or ROWID column name, if the data server supports it.
  def oid_column_name(self, column):
    """ Inputs: 
        Returns: String representing oid, or None if the data server 
                 does not support ROWID.
    """
    return None


  # Returns the converted SA adapter type for a given generic vendor type provided
  def type_descriptor(self, typeobj):
    """ Inputs: generic type to be converted
        Returns: converted adapter type
    """
    return sa_types.adapt_type(typeobj, colspecs)


# A messenger object for a Dialect that corresponds to a single execution.
#   ExecutionContext should have these datamembers:
#   connection
#       Connection object which can be freely used by default value generators to execute SQL. 
#       Should reference the same underlying connection/transactional resources of root_connection.
#   root_connection
#       Connection object which is the source of this ExecutionContext. 
#       May have close_with_result=True set, in which case it can only be used once.
class IBM_DBExecutionContext(default.DefaultExecutionContext):
  """self.statement
     String version of the statement to be executed. Is either passed to the constructor,
     or must be created from the sql.Compiled object by the time pre_exec() has completed.
  """

  """self.parameters
    bind_processor parameters passed to the execute() method. For compiled statements, 
    this is a dictionary or list of dictionaries. For textual statements, it should be 
    in a format suitable for the dialect paramstyle (i.e. dictionary or list of 
    dictionaries for non positional, list or list of lists/tuples for positional).
  """


  # Called after the execution of a statement. This method performs any post-processing required.
  # If the DBSIExecutionContext contains a compiled statement, the last_insert_ids,  
  # last_inserted_params, etc. instance variables should be available after this method completes.
  def post_exec(self):
    """ Inputs: If the ExecutionContext contains a compiled statement, 
                the last_insert_ids, last_inserted_params, etc. instance variables 
                should be available after this method completes.
        Returns: None
    """
    if self.compiled.isinsert and \
       not self.executemany:
      dialect.logger.debug("  >  IBM_DBExecutionContext::post_exec: _last_inserted_ids:" + repr(self._last_inserted_ids))
      if not len(self._last_inserted_ids) or \
         self._last_inserted_ids[0] is None:
        self._last_inserted_ids = [self.cursor.last_identity_val]
    if hasattr( self.compiled , 'offset' ):
        self.cursor.fetchmany( self.compiled.offset )
    

# Compiles ClauseElement objects into SQL strings.
# DefaultCompiler = Default implementation of Compiled.
# Compiled = a compiled SQL expression.
# The __str__ method of the Compiled object should produce the actual text of the statement. 
# Compiled objects are specific to their underlying database dialect, and also may or may not 
# be specific to the columns referenced within a particular set of bind parameters. 
# In no case should the Compiled object be dependent on the actual values of those 
# bind parameters, even though it may reference those values as defaults.
# Compiles ClauseElements into SQL strings.
class IBM_DBCompiler(compiler.DefaultCompiler):

  # Generates the limit/offset clause specific/expected by the database vendor
  def limit_clause(self, select):
    return " fetch first %s rows only" % ( ( select._limit or 0 ) + ( select._offset or 0 ) )
    dialect.logger.debug('\n  ***  IBM_DBCompiler::limit_clause( '+repr(select)+' )')
    return ''

  # Implicit clause to be inserted when no FROM clause is provided
  def default_from(self):
    return " FROM SYSIBM.SYSDUMMY1"   # DB2 uses SYSIBM.SYSDUMMY1 table for row count

  # Generates the SQL string for the SQL function construct.
  def visit_function( self , func ):
    dialect.logger.debug('\n  ***  IBM_DBCompiler::visit_function( '+repr(func.name)+' )')
    if func.name.upper() == "LENGTH":
      return "LENGTH('%s')" % func.compile().params[func.name + '_1']
    else:
      return compiler.DefaultCompiler.visit_function( self, func )

  def visit_select(self, select):
    if select._offset:
        self.offset = select._offset
    return compiler.DefaultCompiler.visit_select(self, select)


# Visitor meant to generate/gather DDL for creating DB objects
class IBM_DBSchemaGenerator(compiler.SchemaGenerator):

  # Overrides default retrieval in the compiler to handle DB2 booleans
  def get_column_default_string(self, column):
    default = compiler.SchemaGenerator.get_column_default_string(self, column)
    if default == "'False'":
      default = '0'
    elif default == "'True'":
      default = '1'
    return default

  # Retrieves the column spec (type, attributes: PK, DEFAULT, NULLABLE)
  def get_column_specification(self, column, first_pk = False):
    """Inputs:  Column object to be specified as a string
                Boolean indicating whether this is the first column of the primary key
       Returns: String, representing the column type and attributes, 
                including primary key, default values, and whether or not it is nullable.
    """
    dialect.logger.debug('\n  ***  IBM_DBSchemaGenerator::get_column_specification( '+repr(column)+' )')

    # column-definition: column-name:
    col_spec = [self.preparer.format_column(column)]
    # data-type:
    col_spec.append(column.type.dialect_impl(self.dialect).get_col_spec())

    # column-options: "NOT NULL"
    if not column.nullable or column.primary_key:
      col_spec.append('NOT NULL')

    # default-clause:
    default = self.get_column_default_string(column)
    if default is not None:
      col_spec.append('WITH DEFAULT')
      if 'str' not in str( column.type ).lower():
        default = default.lstrip("'").rstrip("'")
      col_spec.append(default)

    # generated-column-spec: 

    # identity-options:
    # example:  id INT GENERATED BY DEFAULT AS IDENTITY (START WITH 1),
    if column.primary_key    and \
       column.autoincrement  and \
       isinstance(column.type, sa_types.Integer) and \
       not getattr(self, 'has_IDENTITY', False): # allowed only for a single PK
      col_spec.append('GENERATED BY DEFAULT')
      col_spec.append('AS IDENTITY')
      col_spec.append('(START WITH 1)')
      self.has_IDENTITY = True                   # flag the existence of identity PK

    column_spec = ' '.join(col_spec)
    dialect.logger.debug("\n  ***  IBM_DBSchemaGenerator::get_column_specification: " + str(column_spec))
    return column_spec

  # Defines SQL statement to be executed after table creation
  def post_create_table(self, table):
    if hasattr( self , 'has_IDENTITY' ):    # remove identity PK flag once table is created
      del self.has_IDENTITY
    return ''


# A visitor which generates the DDL used to drop database objects
class IBM_DBSchemaDropper(compiler.SchemaDropper):
  """Generates the string of a sequence to be uses in a DDL DROP statement
     def visit_sequence(self, sequence):
     Inputs:  sequence object representing a SQL Named Sequence 
     Returns: String to be used as a SQL DROP statement for a Named Sequence
  """


# A visitor which accepts ColumnDefault objects, produces the dialect-specific 
# SQL corresponding to their execution, and executes the SQL, returning the result value.
# DefaultRunners are used internally by Engines and Dialects. Specific database modules 
# should provide their own subclasses of DefaultRunner to allow database-specific behavior.
class IBM_DBDefaultRunner(base.DefaultRunner):
  """Retrieves the column default value, if it exists.
     def get_column_default(self, column): pass
     Inputs:  Column object to be specified as a string 
     Returns: column default values as a string, if exists,
              None otherwise
  """
  """Obtains a sequences next value, if it exists, by issuing the appropriate DBSI SQL
     def visit_sequence(self, sequence): pass
     Inputs:  Sequence object representing a SQL Named Sequence 
     Returns: next value of Sequence database object, if exists,
              None otherwise.
  """


# Handle quoting and case-folding of identifiers based on options.
class IBM_DBIdentifierPreparer(compiler.IdentifierPreparer):
  reserved_words = RESERVED_WORDS

  def __init__(self, dialect):
    super(IBM_DBIdentifierPreparer, self).__init__(dialect, initial_quote="'", final_quote="'")

  # Override the identifier quoting default implementation.  
  def _requires_quotes(self, value):
    return False

# Retrieve data server metadata and connection info.
# It is designed to be used in automated configuration tools that expecte
# to query the user for database and connection information
def descriptor():
  """A module-level function that is used by the engine to obtain information
     about adapter. It is designed to be used in automated configuration 
     tools that wish to query the user for database and connection information.
     Returns: dictionary with the following key/value pairs:
              name:  name of the engine, suitable for use in the create_engine function
              description:  plain description of the engine.
              arguments:  dictionary describing the name and description 
                          of each parameter used to connect to the underlying DB-API.
  """
  return { 'name': 'db2',
           'description': 'SQLAlchemy support for IBM Data Servers',
           'arguments': [ ('database', 'Database Name', None),
                          ('schema', 'Schema name', None),
                          ('host', 'Host name', None),
                          ('port', 'Port number', None),
                          ('user', 'Username', None),
                          ('password', 'Password', None)
                         ]
          }

# Set IBM_DBDialect instance attributes: SchemaGenerator, SchemaDropper,
# DefaultRunner, Compiler, IdentifierPreparer, logger
dialect = IBM_DBDialect
dialect.schemagenerator = IBM_DBSchemaGenerator
dialect.schemadropper = IBM_DBSchemaDropper
dialect.defaultrunner = IBM_DBDefaultRunner
dialect.statement_compiler = IBM_DBCompiler
dialect.preparer = IBM_DBIdentifierPreparer
dialect.logger = log.instance_logger(dialect, echoflag=False)
dialect.execution_ctx_cls = IBM_DBExecutionContext