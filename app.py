from flask import Flask

# Create an instance of Flask 
app = Flask(__name__)

# Define a route and the function to handle it
# "/" simboleggia la root
@app.route('/')
def home():
    return "Welcome to the Car Sharing Service!"

@app.route('/about')
def about():
    return "About this page"

@app.route('/user/<username>')
def show_user_profile(username):
    return f"User: {username}"

# Run the application if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
