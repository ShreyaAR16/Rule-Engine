import sqlite3
from datetime import datetime
import json
from rule_engine import dict_to_ast,ast_to_dict

# Initialize and connect to the SQLite database
def init_db():
    conn = sqlite3.connect('rules.db')  # Creates the file 'rules.db' if it doesn't exist
    c = conn.cursor()
    
    # Create the rules table
    c.execute('''
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_string TEXT NOT NULL,
        ast_json TEXT NOT NULL
    )
    ''')
    
    # Create the metadata table
    c.execute('''
    CREATE TABLE IF NOT EXISTS metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_id INTEGER,
        created_at TIMESTAMP,
        modified_at TIMESTAMP,
        FOREIGN KEY (rule_id) REFERENCES rules (id)
    )
    ''')

    conn.commit()
    conn.close()

# Call this function to initialize the database when the app starts

def insert_rule(rule_string, ast_node):
    """
    Inserts a rule into the database.
    :param rule_string: The original rule as a string.
    :param ast_node: The ASTNode object representing the rule.
    """
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    
    # Convert the ASTNode to a JSON string using ast_to_dict
    ast_json = json.dumps(ast_to_dict(ast_node))
    
    # Insert the rule into the rules table
    c.execute('''
        INSERT INTO rules (rule_string, ast_json) VALUES (?, ?)
    ''', (rule_string, ast_json))
    
    rule_id = c.lastrowid  # Get the id of the inserted rule
    
    # Insert metadata (timestamps) into the metadata table
    created_at = modified_at = datetime.now()
    c.execute('''
        INSERT INTO metadata (rule_id, created_at, modified_at) VALUES (?, ?, ?)
    ''', (rule_id, created_at, modified_at))
    
    conn.commit()
    conn.close()

    return rule_id  # Return the rule's ID for further reference

def get_rule(rule_id):
    """
    Retrieves a rule from the database by its ID.
    :param rule_id: The ID of the rule to retrieve.
    :return: A tuple containing the rule string and the ASTNode object.
    """
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    
    # Retrieve the rule by ID
    c.execute('SELECT rule_string, ast_json FROM rules WHERE id = ?', (rule_id,))
    row = c.fetchone()
    
    conn.close()
    
    if row:
        rule_string = row[0]
        ast_json = row[1]
        ast_node = dict_to_ast(json.loads(ast_json))  # Convert JSON back to ASTNode
        return rule_string, ast_node
    else:
        return None

def update_rule(rule_id, new_rule_string, new_ast_node):
    """
    Updates an existing rule in the database.
    :param rule_id: The ID of the rule to update.
    :param new_rule_string: The updated rule string.
    :param new_ast_node: The updated ASTNode object.
    """
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    
    # Convert the new ASTNode to a JSON string
    new_ast_json = json.dumps(ast_to_dict(new_ast_node))
    
    # Update the rule and the modified timestamp
    modified_at = datetime.now()
    c.execute('''
        UPDATE rules
        SET rule_string = ?, ast_json = ?
        WHERE id = ?
    ''', (new_rule_string, new_ast_json, rule_id))
    
    # Update the metadata
    c.execute('''
        UPDATE metadata
        SET modified_at = ?
        WHERE rule_id = ?
    ''', (modified_at, rule_id))
    
    conn.commit()
    conn.close()
