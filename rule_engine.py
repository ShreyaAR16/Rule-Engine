class ASTNode:
    def __init__(self, type, left=None, right=None, value=None):
        """
        Initialize the ASTNode.

        :param type: "operator" (for AND/OR) or "operand" (for conditions)
        :param left: Left child node
        :param right: Right child node
        :param value: Value of the operand (e.g., 'age > 30')
        """
        self.type = type
        self.left = left
        self.right = right
        self.value = value

def create_rule(rule_string):
    """
    Parse a rule string and return an ASTNode (root node of the tree).
    This implementation is dynamic and can handle different attributes.
    
    Example:
    "age > 30 AND department == 'Sales'"
    """
    # Split the rule by "AND" or "OR" and build the AST dynamically
    if ' AND ' in rule_string:
        operator = 'AND'
        left_rule, right_rule = rule_string.split(' AND ', 1)
    elif ' OR ' in rule_string:
        operator = 'OR'
        left_rule, right_rule = rule_string.split(' OR ', 1)
    else:
        # It's a single condition (operand)
        return ASTNode('operand', value=rule_string.strip())

    # Recursively create the AST for the left and right conditions
    root = ASTNode('operator', value=operator)
    root.left = create_rule(left_rule)
    root.right = create_rule(right_rule)
    
    return root

def combine_rules(rules, operator="AND"):
    """
    Combines multiple rule ASTs into a single AST using the specified operator (AND/OR).
    """
    if not rules:
        return None

    # Start with the first rule
    root = rules[0]
    
    # Combine the rest of the rules with the operator
    for i in range(1, len(rules)):
        root = ASTNode('operator', value=operator, left=root, right=rules[i])

def evaluate_rule(rule_ast, data):
    """
    Evaluate the AST against the given data.

    :param rule_ast: The root of the AST (parsed rule)
    :param data: A dictionary containing the user data (e.g., {"age": 35, "department": "Sales"})
    :return: True if the rule is satisfied, False otherwise
    """
    if rule_ast.type == 'operand':
        # Get the condition string from the AST node (e.g., 'age > 30')
        condition = rule_ast.value
        
        # Dynamically replace variable names in the condition with their values from the data
        for key, value in data.items():
            if isinstance(value, str):
                # If the value is a string, we need to add quotes around it for evaluation
                condition = condition.replace(key, f"'{value}'")
            else:
                # For numbers and other types, just replace directly
                condition = condition.replace(key, str(value))

        print(f"Evaluating condition: {condition}")  # For debugging
        
        # Safely evaluate the condition (the condition now contains actual values)
        return eval(condition)
    
    elif rule_ast.type == 'operator':
        if rule_ast.value == 'AND':
            return evaluate_rule(rule_ast.left, data) and evaluate_rule(rule_ast.right, data)
        elif rule_ast.value == 'OR':
            return evaluate_rule(rule_ast.left, data) or evaluate_rule(rule_ast.right, data)

def ast_to_dict(ast_node):
    """Convert an ASTNode to a dictionary for serialization."""
    if not ast_node:
        return None
    
    return {
        "type": ast_node.type,
        "left": ast_to_dict(ast_node.left),
        "right": ast_to_dict(ast_node.right),
        "value": ast_node.value
    }

def dict_to_ast(data):
    """Convert a dictionary back to an ASTNode."""
    if not data:
        return None
    
    return ASTNode(
        type=data['type'],
        left=dict_to_ast(data.get('left')),
        right=dict_to_ast(data.get('right')),
        value=data.get('value')
    )

if __name__ == "__main__":
    # Example rule: "age > 30 AND department == 'Sales'"
    rule_string = "age > 30 AND department == 'Sales'"
    
    # Create the AST for the rule
    rule_ast = create_rule(rule_string)
    
    # Define some test data
    user_data = {"age": 35, "department": "Sales"}
    
    # Evaluate the rule against the user data
    result = evaluate_rule(rule_ast, user_data)
    
    print(f"Result of rule evaluation: {result}")  # Should print True
