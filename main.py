# Imports
from flask import Flask, render_template, url_for, redirect, jsonify
from flask_bootstrap import Bootstrap5
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Setting up flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
# Bootstrap setup
Bootstrap5(app)

# Setting up Pymongo database
client = MongoClient() # ('localhost', 27017)
db = client["Hardware"]
hardware_collection = db['hardwareComponents']
software_collection = db['softwareProducts']
peripheral_collection = db['peripheralDevices']

# # Accessing the json data for the database
# import json
# with open("./static/Hardware.json", mode="r") as file:
#     data = json.load(file)

# # Populating the collections using the json data provided
# hardware_collection.insert_many(data["hardwareComponents"])
# software_collection.insert_many(data["softwareProducts"])
# peripheral_collection.insert_many(data["peripheralDevices"])

# Updated the dataset to have colors array for multiple peripheral documents
# Updated the dataset to have embedded documents inside an array called versions attached to documents in the software collection


# Add and edit items form
class CreateItemForm(FlaskForm):
    componentName = StringField("Component Name", validators=[DataRequired()])
    componentType = StringField("Component Type", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    manufacturer = StringField("Manufacturer", validators=[DataRequired()])
    compatibility = StringField("Compatibility", validators=[DataRequired()])
    submit = SubmitField("Submit Item")


# Iterate over result sets
# default route, Show all items
@app.route('/')
def get_all_items():
    # Obtaining hardware collection
    hardware_items = list(hardware_collection.find())  # Fetching from the hardware collection
    for item in hardware_items:
        item["_id"] = str(item["_id"])
    # Obtaining software collection
    software_items = list(software_collection.find())  # Fetching from the hardware collection
    for item in software_items:
        item["_id"] = str(item["_id"])
    # Obtaining peripheral collection
    peripheral_items = list(peripheral_collection.find())  # Fetching from the hardware collection
    for item in peripheral_items:
        item["_id"] = str(item["_id"])
    return render_template("index.html", hardware_items=hardware_items, software_items=software_items, peripheral_items=peripheral_items)


# Show single item
@app.route("/item/<id>")
def show_item(id):
    # Obtaining hardware collection
    hardware_item = hardware_collection.find_one({"_id": ObjectId(id)})  # Fetching from the hardware collection
    if hardware_item:
        hardware_item["_id"] = str(hardware_item["_id"])
    # Obtaining software collection
    software_item = software_collection.find_one({"_id": ObjectId(id)})  # Fetching from the hardware collection
    if software_item:
        software_item["_id"] = str(software_item["_id"])
    # Obtaining peripheral collection
    peripheral_item = peripheral_collection.find_one({"_id": ObjectId(id)})  # Fetching from the hardware collection
    if peripheral_item:
        peripheral_item["_id"] = str(peripheral_item["_id"])
    return render_template("item.html", hardware_item=hardware_item, peripheral_item=peripheral_item, software_item=software_item)


# Create item
@app.route("/new-item", methods=["GET", "POST"])
def add_document():
    form = CreateItemForm()
    if form.validate_on_submit():
        item = {
            "componentName": form.componentName.data,
            "componentType": form.componentType.data,
            "price": form.price.data,
            "manufacturer": form.manufacturer.data,
            "compatibility": form.compatibility.data
        }
        hardware_collection.insert_one(item)
        return redirect(url_for("get_all_items"))
    return render_template("add.html", form=form)


# Update an item
@app.route('/update-specific-item/<id>', methods=["GET", 'POST'])
def edit_item(id):
    item = hardware_collection.find_one({"_id": ObjectId(id)})  # Fetching from the hardware collection
    if item:
        item["_id"] = str(item["_id"])
    edit_form = CreateItemForm(
        componentName=item["componentName"],
        componentType=item["componentType"],
        price=item["price"],
        manufacturer=item["manufacturer"],
        compatibility=item["compatibility"]
    )
    if edit_form.validate_on_submit():
        update_values = {
            "componentName": edit_form.componentName.data,
            "componentType": edit_form.componentType.data,
            "price": edit_form.price.data,
            "manufacturer": edit_form.manufacturer.data,
            "compatibility": edit_form.compatibility.data
        }
        result = hardware_collection.update_one({"_id": ObjectId(id)}, {"$set": update_values})
        return redirect(url_for("show_item", id=item["_id"]))
    return render_template("add.html", form=edit_form, is_edit=True)


# Query 13, Conditional Update
# @app.route('/query13')
# def query13():
#     query = {"deviceName": "Logitech C922 Pro Stream"} # Returns an item based on its device name
#     update = {"compatability": "USB-C"} # updating compatibility to USB-C
#     result = peripheral_collection.update_one(query, update)
#     return {"updated_compatibility": result}


# Delete an item
@app.route('/delete-item/<id>')
def delete_item(id):
    item = hardware_collection.delete_one({"_id": ObjectId(id)})  # Deleting from the hardware collection

    if item.deleted_count:
        return redirect(url_for('get_all_items'))
    else:
        return jsonify({"message": "Item not found."}), 404


# Query 1, Select Only necessary fields
@app.route('/query1')
def query1():
    title = "Query1"
    description = "Returning only the componentName and componentType Fields from the Hardware Collection"
    projection = {"componentName": 1, "componentType": 1} # Specifying the fields I want returned
    items = list(hardware_collection.find({}, projection)) # Creating a list of items out of the result
    for item in items:
        item["_id"] = str(item["_id"]) # Converting Objectid to string
    return render_template("results.html", description=description, title=title, items=items)


# Query 2, Match values in an array
@app.route('/query2')
def query2():
    title = "Query2"
    description = "Only returning items that come in black from the Peripheral Collection"
    # Alternatively, query = {"colour": {"$in": ["black", "white"]}} # Finds documents with black and white present ($in for present, $ne for absent)
    query = {"colour":"black"} # Finding documents with arrays that mention the colour black
    items = list(peripheral_collection.find(query)) # Creating a list of items out of the result
    for item in items:
        item["_id"] = str(item["_id"]) # Converting Objectid to string
    return render_template("results.html", description=description, title=title, items=items)

# Query 3, Match array elements with multiple criteria
# Query 6, Query embedded documents and arrays
    # query = {"version.supported":"True"}
# Query 7, Match elements in arrays with criteria
@app.route('/query3')
def query3():
    title = "Query3"
    description = "Only returning items with supported versions and file sizes greater than 50MB from the Software Collection"
    # This query matches documents using their versions array based on if supported is true and if the size is greater than 50
    query = {"version": {"$elemMatch": {"supported":"True", "size": {"$gte":50}}}}
    items = list(software_collection.find(query))  # Creating a list of items out of the result
    for item in items:
        item["_id"] = str(item["_id"])  # Converting Objectid to string
    return render_template("results.html", description=description, title=title, items=items)


# Query 4, Match arrays containing all specified elements
@app.route('/query4')
def query4():
    title = "Query4"
    description = "Listing all items that come in the colours Black, Blue and White from the Peripheral Collection"
    # The below query will list all documents in the peripheral collection which have colour arrays that contain all the listed colours.
    query = {"colour": {"$all": ["black","blue", "white"]}}
    items = list(peripheral_collection.find(query))  # Creating a list of items out of the result
    for item in items:
        item["_id"] = str(item["_id"])  # Converting Objectid to string
    return render_template("results.html", description=description, title=title, items=items)


@app.route('/query5')
def query5():
    title = "Query5"
    description = "Using the Peripheral Collection. Creates a new field that combines the device name and type. Removing any items with a price greater than 140. Unwinding the colour options into seperate documents. "
    pipeline = [
        {
            '$addFields': {
                'full_title': {
                    '$concat': ['$deviceName', ' ', '$deviceType']
                }
            }
        }, # Adds a new field called full title that combines the device name and type
        {"$match": {"price": {"$lte": 140}}}, # Removing any items with a price greater than 140
        {"$unwind": "$colour"},  # Turns each peripherals colour variants into their own documents
        # {"$group": {"_id": "$deviceName"}} # Grouping these documents using the device names
    ]
    items = list(peripheral_collection.aggregate(pipeline))
    for item in items:
        item["_id"] = str(item["_id"])  # Converting Objectid to string
    return render_template("results.html", description=description, title=title, items=items)


# Query 8, Match arrays with all elements specified
@app.route('/query8')
def query8():
    title = "Query8"
    description = "Returns all documents with versions both not supported and less than 300MB from the Software Collection"
    # This query matches documents inside the versions array using the $all operator if they are no longer supported
    query = {"version": {"$all": [{"$elemMatch": {"supported": "False"}}, {"$elemMatch": {"size":{"$lt":300}}}]}}
    items = list(software_collection.find(query))  # Creating a list of items out of the result
    for item in items:
        item["_id"] = str(item["_id"])  # Converting Objectid to string
    return render_template("results.html", description=description, title=title, items=items)


# Query 9, Perform text search
@app.route('/query9')
def query9():
    title = "Query9"
    description = "Returns any item with the text NVIDIA in their name from the Hardware Collection"
    hardware_collection.create_index({"componentName": "text"})
    query = {'$text': {'$search': 'NVIDIA'}} # Returns results with the text NVIDIA
    items = list(hardware_collection.find(query))
    for item in items:
        item["_id"] = str(item["_id"])  # Converting Objectid to string
    return render_template("results.html", description=description, title=title, items=items)


# Query 10, Perform a left outer join
@app.route('/query10')
def query10():
    title = "Query10"
    description = "Joining the hardware and peripheral collection"
    # Using the collections for hardware and peripherals
    pipeline = [
        {
            '$lookup': {
                'from': 'peripheral_collection',  # collection to join
                'localField': '_id',  # field from the input documents
                'foreignField': '_id',  # field from the documents of the "from" collection
                'as': 'products'  # output array field
            }
        },
        {
            '$unwind': {
                'path': '$products',
                'preserveNullAndEmptyArrays': True # because the default behavior for $unwind is to omit documents where the referenced field is missing or an empty array
            }
        }
    ]
    hardware_with_peripherals = list(hardware_collection.aggregate(pipeline))
    for item in hardware_with_peripherals:
        item["_id"] = str(item["_id"])  # Converting Objectid to string
    return render_template("results.html", description=description, title=title, items=hardware_with_peripherals)


# Query 11, Data transformations
@app.route('/query11')
def query11():
    title = "Query11"
    description = "Add a new field 'full_title' by concatenating componentName and componentType"
    # Add a new field 'full_title' by concatenating componentName and componentType
    pipeline = [
        {
            '$addFields': {
                'full_title': {
                    '$concat': ['$componentName', ' ', '$componentType']
                }
            }
        }
    ]
    transformed_data = list(hardware_collection.aggregate(pipeline))
    for item in transformed_data:
        item["_id"] = str(item["_id"])  # Converting Objectid to string
    return render_template("results.html", description=description, title=title, items=transformed_data)


# Query 12, Deconstruct array into separate documents
@app.route('/query12')
def query12():
    title = "Query12"
    description = "Using the Peripheral Collection. Breaking product colours into seperate items"
    pipeline = [
        # Taking each colour in the colour array and creating separate documents.
        {'$unwind': '$colour'},
    ]
    deconstructed_items = list(peripheral_collection.aggregate(pipeline))
    for item in deconstructed_items:
        item["_id"] = str(item["_id"])  # Converting Objectid to string
    return render_template("results.html", description=description, title=title, items=deconstructed_items)


# Query 13, MapReduce
@app.route('/query13')
def query13():
    # # Define the map function
    # # The map function is called once for each document in the collection. Each call to the map function emits a key-value pair
    # # The component name is the key and the price is the value
    # map_function = Code("function() { emit(this.componentName, this.price); }")
    # # Define the reduce function
    # # The reduce function is called once for each unique key emitted by the map function. It combines all the values for that key to a single result
    # reduce_function = Code("function(keyComponentName, valuesPrice)")
    # # Run the MapReduce function
    # price_per_component = hardware_collection.map_reduce(map_function, reduce_function, "price_per_component") # Results in a price_per_component collection.
    # # Prepare and send the response
    # component_prices = price_per_component.find()
    title = "Query13"
    description = "Map Reduce like Function"
    pipeline = [
        {"$group": {"_id": "$componentName", "price": {"$sum": "$price"}}},
        {"$sort": {"_id": 1}}
    ]
    component_prices = list(hardware_collection.aggregate(pipeline))
    return jsonify(component_prices)


# Query 14, Use aggregation Expressions
@app.route('/query14')
def query14():
    title = "Query14"
    description = "Calculate the total number of Products from each Manufacturer in the Hardware Collection"
    # Calculate the total number of Products from each Manufacturer
    pipeline = [
        {
            '$group': {
                '_id': '$manufacturer',
                'total_products': {'$sum': 1}
            }
        }
    ]
    product_totals = list(hardware_collection.aggregate(pipeline))
    return render_template("results.html", description=description, title=title, items=product_totals)


if __name__ == "__main__":
    app.run(debug=True)
