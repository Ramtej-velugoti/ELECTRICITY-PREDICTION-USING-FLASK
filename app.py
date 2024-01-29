from flask import Flask, request, render_template
import pickle

# Importing models
model = pickle.load(open('Household_energy_bill_data.pkl', 'rb'))

# Creating Flask app
app = Flask(__name__)

def get_message(result):
    return result

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Retrieve form data
        if 'num_rooms' in request.form:
            num_rooms = float(request.form['num_rooms'])
            num_people = float(request.form['num_people'])
            housearea = float(request.form['housearea'])
            is_ac = float(request.form['is_ac'])
            is_tv = float(request.form['is_tv'])
            is_flat = float(request.form['is_flat'])
            ave_monthly_income = float(request.form['ave_monthly_income'])
            num_children = float(request.form['num_children'])
            is_urban = float(request.form['is_urban'])
            

            # Perform prediction
            feature_list = [num_rooms, num_people, housearea, is_ac,
                            is_tv, is_flat, ave_monthly_income,
                            num_children, is_urban]

            prediction = model.predict([feature_list])
        
            # Process prediction result
            if prediction[0]:
                result = "{:.2f} %".format(prediction[0])
                message = get_message(prediction[0])
            else:
                result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
                message = "Error: {}".format(result)
    except Exception as e:
        result = "Error processing the prediction: {}".format(str(e))
        message = "Error: {}".format(result)

    return render_template('index.html', result=result, message=message)




# Python main
if __name__ == "__main__":
    app.run(debug=True)
