# Database MCP Servers

This directory contains Model Context Protocol (MCP) servers that **enable LLMs to directly execute database queries using native query languages**. These servers provide seamless database access, allowing AI assistants like Claude to read and write data using SQL (SQLite) and Cypher (Neo4j) without requiring users to know the query syntax.

## 🎯 Core Capability

**Direct Query Language Execution**: LLMs can write and execute database queries in their native languages:
- **SQL queries** for relational data operations (SQLite)
- **Cypher queries** for graph data operations (Neo4j)

The AI assistant handles the query construction, execution, and result interpretation, making database operations accessible through natural language conversations.

## Available Servers

### 🗃️ SQLite MCP Server
**Path:** `sqlite/`  
**Language:** Python  
**Database:** SQLite  
**Query Language:** SQL

Enables LLMs to execute SQL queries directly against SQLite databases for comprehensive relational data operations.

#### Core Database Operations
- **Read Operations**: `SELECT` queries with joins, aggregations, filtering
- **Write Operations**: `INSERT`, `UPDATE`, `DELETE` for data manipulation
- **Schema Operations**: `CREATE TABLE`, `ALTER TABLE` for structure management
- **Query Analysis**: Automatic query optimization and result interpretation

#### Enhanced Features
- **Business Intelligence**: Generate insights and maintain living business memos
- **Interactive Demos**: Built-in demo prompts for learning database concepts
- **Schema Introspection**: Automatic table discovery and structure analysis

#### Tools Available
- `read_query` - Execute any SELECT query to read data
- `write_query` - Execute INSERT, UPDATE, DELETE queries
- `create_table` - Execute CREATE TABLE statements
- `list_tables` - Discover available tables
- `describe_table` - View table schema and structure
- `append_insight` - Add business insights to analysis memo

### 🔗 Neo4j MCP Server
**Path:** `neo4j-mcp/`  
**Language:** TypeScript (Bun)  
**Database:** Neo4j Graph Database  
**Query Language:** Cypher

Enables LLMs to execute Cypher queries directly against Neo4j databases for graph data operations and analysis.

#### Core Graph Operations
- **Node Operations**: `CREATE`, `MATCH`, `MERGE` for entity management
- **Relationship Operations**: Create and query complex relationships
- **Pattern Matching**: Advanced graph pattern queries
- **Path Analysis**: Shortest paths, traversals, and graph algorithms

#### Enhanced Features
- **Connection Management**: Multiple connection methods with status monitoring
- **Type Transformation**: Automatic Neo4j to JavaScript object conversion
- **Database Introspection**: Real-time database metrics and schema discovery
- **Query Optimization**: Parameter binding and performance monitoring

#### Tools Available
- `Connect` - Establish database connection with credentials
- `ConnectWithEnv` - Connect using environment variables
- `Query` - **Execute any Cypher query directly**
- `GetDatabaseInfo` - Retrieve database schema and statistics
- `GetConnectionStatus` - Monitor connection health
- `Disconnect` - Clean connection termination

## 🚀 Direct Query Examples

### SQL Query Execution (SQLite)
The LLM can directly write and execute SQL queries:

```sql
-- Complex analytical query the LLM might generate
SELECT 
    c.name,
    COUNT(o.id) as order_count,
    SUM(o.total) as total_spent,
    AVG(o.total) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.order_date >= date('now', '-30 days')
GROUP BY c.id, c.name
HAVING total_spent > 1000
ORDER BY total_spent DESC;

-- Data insertion the LLM might perform
INSERT INTO products (name, price, category, stock)
VALUES 
    ('Gaming Laptop', 1299.99, 'Electronics', 15),
    ('Wireless Mouse', 29.99, 'Electronics', 50);
```

### Cypher Query Execution (Neo4j)
The LLM can directly write and execute Cypher queries:

```cypher
// Complex graph pattern matching the LLM might generate
MATCH (person:Person)-[:FRIENDS_WITH]-(friend:Person)
WHERE person.age > 25
WITH person, collect(friend) as friends
MATCH (person)-[:WORKS_FOR]->(company:Company)
RETURN person.name, company.name, size(friends) as friend_count
ORDER BY friend_count DESC;

// Graph data creation the LLM might perform
CREATE (alice:Person {name: 'Alice', age: 30, email: 'alice@example.com'})
CREATE (bob:Person {name: 'Bob', age: 28, email: 'bob@example.com'})
CREATE (techcorp:Company {name: 'TechCorp', industry: 'Technology'})
CREATE (alice)-[:FRIENDS_WITH]->(bob)
CREATE (alice)-[:WORKS_FOR]->(techcorp)
CREATE (bob)-[:WORKS_FOR]->(techcorp);
```

## Installation & Setup

### SQLite MCP Server

#### Prerequisites
- Python 3.10 or higher
- uv (recommended) or pip

#### Installation
```bash
cd src/saaga_mcp_servers/db/sqlite

# Using uv (recommended)
uv install

# Or using pip
pip install -e .
```

#### Configuration for Claude Desktop
```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uv",
      "args": [
        "--directory",
        "path/to/src/saaga_mcp_servers/db/sqlite",
        "run",
        "mcp-server-sqlite",
        "--db-path",
        "~/my_database.db"
      ]
    }
  }
}
```

#### Docker Usage
```bash
# Build
docker build -t mcp/sqlite .

# Run
docker run --rm -i -v mcp-data:/mcp mcp/sqlite --db-path /mcp/database.db
```

### Neo4j MCP Server

#### Prerequisites
- [Bun](https://bun.sh/) v1.0.0 or higher
- Neo4j database (local or remote)

#### Installation
```bash
cd src/saaga_mcp_servers/db/neo4j-mcp

# Install dependencies
bun install

# Build for production
bun run build
```

#### Environment Configuration
Create a `.env` file:
```env
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
NODE_ENV=development
```

#### Running Neo4j with Docker
A `docker-compose.yml` is included for easy Neo4j setup:
```bash
# Start Neo4j
docker-compose up -d

# Access Neo4j Browser at http://localhost:7474
# Default credentials: neo4j/your_password

# Stop Neo4j
docker-compose down
```

#### Configuration for Claude Desktop
```json
{
  "mcpServers": {
    "neo4j": {
      "command": "path/to/src/saaga_mcp_servers/db/neo4j-mcp/mcp-wrapper.sh"
    }
  }
}
```

## 💡 LLM Query Capabilities

### What LLMs Can Do

#### **SQLite (SQL) Operations**
- **Data Analysis**: Complex SELECT queries with JOINs, aggregations, window functions
- **Data Manipulation**: INSERT, UPDATE, DELETE operations with conditional logic
- **Schema Management**: CREATE/ALTER tables, indexes, and constraints
- **Business Intelligence**: Analytical queries for insights and reporting
- **Data Validation**: Queries to check data quality and consistency

#### **Neo4j (Cypher) Operations**
- **Graph Exploration**: Pattern matching to discover relationships and paths
- **Social Network Analysis**: Friend networks, influence mapping, community detection
- **Recommendation Systems**: Collaborative filtering and similarity queries
- **Path Finding**: Shortest paths, route optimization, network analysis
- **Data Modeling**: Create complex graph structures with multiple node types

### Example Conversation Flow

```
User: "Show me the top customers by revenue in the last quarter"

LLM: I'll query the database to find your top customers by revenue.

[Executes SQL]:
SELECT c.name, SUM(o.total) as total_revenue
FROM customers c
JOIN orders o ON c.id = o.customer_id  
WHERE o.order_date >= date('now', '-3 months')
GROUP BY c.id, c.name
ORDER BY total_revenue DESC
LIMIT 10;

[Returns results and analysis]
```

## Advanced Features

### SQLite Business Intelligence
- **Automatic Query Generation**: LLM creates optimized SQL based on natural language requests
- **Insight Discovery**: Automated pattern recognition and anomaly detection
- **Living Documentation**: Dynamic memo updates with discovered insights
- **Interactive Analysis**: Guided exploration of data relationships

### Neo4j Graph Intelligence  
- **Relationship Discovery**: Automatic identification of important graph patterns
- **Network Analysis**: Centrality measures, clustering, and community detection
- **Query Optimization**: Parameter binding and efficient traversal strategies
- **Real-time Monitoring**: Connection health and query performance tracking

## Development

### SQLite Server
```bash
cd src/saaga_mcp_servers/db/sqlite

# Development with hot reload
uv run mcp-server-sqlite --db-path test.db

# Run tests (if available)
uv run pytest
```

### Neo4j Server
```bash
cd src/saaga_mcp_servers/db/neo4j-mcp

# Development mode
bun run dev

# Build production bundle
bun run build

# Run tests
bun test
```

## Troubleshooting

### Common SQLite Issues
- **Permission errors**: Ensure write access to database file location
- **Database locked**: Close other connections to the database
- **Query syntax**: LLM will handle SQL syntax, but check for schema mismatches

### Common Neo4j Issues
- **Connection refused**: Check if Neo4j is running on specified port
- **Authentication failed**: Verify username/password in environment variables
- **Query timeout**: Complex graph traversals may need optimization

### Query Debugging
- **SQLite**: Use `EXPLAIN QUERY PLAN` for query optimization insights
- **Neo4j**: Use `PROFILE` or `EXPLAIN` to analyze Cypher query performance
- Both servers provide detailed error messages for debugging

## License

Both MCP servers are licensed under the MIT License. See individual project directories for specific license files.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

For issues or feature requests, please use the project's issue tracker.
