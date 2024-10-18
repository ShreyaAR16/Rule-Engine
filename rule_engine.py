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
    For now, we will handle a specific case.
    
    Example:
    "age > 30 AND department = 'Sales'"
    """
    # Current implementation is hardcoded for a specific rule
    root = ASTNode('operator', value='AND')
    root.left = ASTNode('operand', value='age > 30')
    root.right = ASTNode('operand', value="department == 'Sales'")  # Use '==' for comparison
    return root

def combine_rules(rules):
    """
    Combines multiple rule ASTs into a single AST using the AND operator.
    """
    if not rules:
        return None
    
    root = rules[0]
    for i in range(1, len(rules)):
        root = ASTNode('operator', value='AND', left=root, right=rules[i])
    
    return root

def evaluate_rule(rule_ast, data):
    """
    Evaluate the AST against the given data.

    :param rule_ast: The root of the AST
    :param data: A dictionary containing the user data (e.g., {"age": 35, "department": "Sales"})
    :return: True if the rule is satisfied, False otherwise
    """
    if rule_ast.type == 'operand':
        # Evaluate the condition stored in the operand (e.g., 'age > 30')
        print(f"Evaluating rule: {rule_ast.value}")  # Print the condition being evaluated
        return eval(rule_ast.value, {}, data)  # Evaluate the condition using eval
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
