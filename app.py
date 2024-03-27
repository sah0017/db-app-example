from core import app
from flask import redirect, request 
from flask.templating import render_template
from models import Actor, ActorInfo

# A decorator used to tell the application 
# which URL is associated with which function 
@app.route('/hello')	 
def hello(): 
	return 'HELLO'

# APP ROUTE TO GET RESULTS FOR SELECT QUERY 
@app.route('/get_actors', methods=['GET','POST']) 
def get_results(): 
    actors = Actor.get_actors()  
    return actors 

# APP ROUTE TO RENDER HOME PAGE WITH LIST OF ACTORS
@app.route('/')
def index():
	# Query all data and then pass it to the template
	actors = Actor.get_actors()
	return render_template('index.html', actors=actors)

# APP ROUTE TO RENDER FORM TO ADD ACTOR DATA
@app.route('/add_data')
def add_data():
	return render_template('add_actor.html')

# APP ROUTE TO CALL FUNCTION TO ADD ACTOR
@app.route('/add', methods=["POST"])
def add_actor():
	
	# In this function we will input data from the 
	# form page and store it in our database.
	# Remember that inside the get the name should
	# exactly be the same as that in the html
	# input fields
	first_name = request.form.get("first_name")
	last_name = request.form.get("last_name")

	# call model function that will store data as a row in our datatable
	if first_name != '' and last_name != '':
		Actor.add_actor(first_name, last_name)
		return redirect('/')
	else:
		return redirect('/')

# APP ROUTE TO CALL FUNCTION TO DELETE ACTOR
@app.route('/delete/<int:id>')
def delete_actor(id):
	# Deletes the data on the basis of unique id and 
	# redirects to home page
	Actor.delete_actor(id)
	return redirect('/')

# APP ROUTE TO CALL FUNCTION TO RETRIEVE AND RETURN ACTOR INFO
@app.route('/actor_info')
def get_actor_info():
	return ActorInfo.get_actor_info()

if __name__=='__main__': 
    app.run(port=8000, debug=True) 


