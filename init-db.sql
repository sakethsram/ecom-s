-- Create databases if they don't exist
CREATE DATABASE IF NOT EXISTS amazon_bookstore;
CREATE DATABASE IF NOT EXISTS flipkart_bookstore;
CREATE DATABASE IF NOT EXISTS sapna_bookstore;

-- Grant permissions (optional, but good practice)
GRANT ALL PRIVILEGES ON amazon_bookstore.* TO 'root'@'%';
GRANT ALL PRIVILEGES ON flipkart_bookstore.* TO 'root'@'%';
GRANT ALL PRIVILEGES ON sapna_bookstore.* TO 'root'@'%';
FLUSH PRIVILEGES;