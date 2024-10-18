from flask import Flask, request, jsonify, render_template
from rule_engine import create_rule, combine_rules, evaluate_rule, dict_to_ast, ast_to_dict
from database import init_db,insert_rule, get_rule, update_rule

app = Flask(__name__)

# Route to create and return the AST for a rule string
@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    data = request.json
    rule_string = data.get('rule')
    
    if not rule_string:
        return jsonify({"error": "Rule string is required"}), 400
    
    # Create the AST for the given rule
    rule_ast = create_rule(rule_string)

    # Insert the rule into the database
    rule_id = insert_rule(rule_string, rule_ast)
    
    # Serialize the AST to a dictionary before returning it
    return jsonify({"rule_id": rule_id,"rule_ast": ast_to_dict(rule_ast)}), 200



@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    data = request.json
    rules = data.get('rules')
    
    if not rules or not isinstance(rules, list):
        return jsonify({"error": "A list of rules is required"}), 400
    
    rule_asts = [create_rule(rule_string) for rule_string in rules]
    combined_ast = combine_rules(rule_asts)
    
    # Return the combined AST as a serialized dictionary
    return jsonify({"combined_ast": ast_to_dict(combined_ast)}), 200


@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    data = request.json
    rule_ast_data = data.get('rule_ast')  # This should be a dictionary
    user_data = data.get('user_data')  # Extract the user data
    
    if not rule_ast_data or not user_data:
        return jsonify({"error": "Rule AST and user data are required"}), 400
    
    # Deserialize the AST dictionary back to an ASTNode object
    rule_ast = dict_to_ast(rule_ast_data)
    
    # Evaluate the rule AST against the user data
    result = evaluate_rule(rule_ast, user_data)
    
    # Return the result (True or False) as a JSON response
    return jsonify({"result": result}), 200

@app.route('/add_rule', methods=['POST'])
def add_rule_api():
    data = request.json
    rule_string = data.get('rule')
    ast_structure = str(create_rule(rule_string))
    
    # Save rule to database
    insert_rule(rule_string, ast_structure)
    
    return jsonify({"message": "Rule saved successfully"}), 201

@app.route('/get_rules', methods=['GET'])
def get_rules_api():
    rules = get_rule()
    return jsonify({"rules": rules}), 200


@app.route('/evaluate_rule_from_db/<int:rule_id>', methods=['POST'])
def evaluate_rule_from_db(rule_id):
    data = request.json
    user_data = data.get('user_data')
    
    if not user_data:
        return jsonify({"error": "User data is required"}), 400
    
    # Retrieve the rule from the database by ID
    rule_info = get_rule(rule_id)
    if rule_info is None:
        return jsonify({"error": "Rule not found"}), 404
    
    rule_string, rule_ast = rule_info
    
    # Evaluate the rule against the user data
    result = evaluate_rule(rule_ast, user_data)
    
    return jsonify({"result": result}), 200

@app.route('/update_rule/<int:rule_id>', methods=['PUT'])
def update_rule_api(rule_id):
    data = request.json
    new_rule_string = data.get('rule')
    
    if not new_rule_string:
        return jsonify({"error": "Rule string is required"}), 400
    
    # Create the new AST for the updated rule
    new_rule_ast = create_rule(new_rule_string)
    
    # Update the rule in the database
    update_rule(rule_id, new_rule_string, new_rule_ast)
    
    return jsonify({"message": "Rule updated successfully", "rule_id": rule_id}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)

