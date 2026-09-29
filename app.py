from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load("Flood_Prediction_Model.pkl")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "POST":

        data = [[
            int(request.form["MonsoonIntensity"]),
            int(request.form["TopographyDrainage"]),
            int(request.form["RiverManagement"]),
            int(request.form["Deforestation"]),
            int(request.form["Urbanization"]),
            int(request.form["ClimateChange"]),
            int(request.form["DamsQuality"]),
            int(request.form["Siltation"]),
            int(request.form["AgriculturalPractices"]),
            int(request.form["Encroachments"]),
            int(request.form["IneffectiveDisasterPreparedness"]),
            int(request.form["DrainageSystems"]),
            int(request.form["CoastalVulnerability"]),
            int(request.form["Landslides"]),
            int(request.form["Watersheds"]),
            int(request.form["DeterioratingInfrastructure"]),
            int(request.form["PopulationScore"]),
            int(request.form["WetlandLoss"]),
            int(request.form["InadequatePlanning"]),
            int(request.form["PoliticalFactors"])
        ]]

        columns = [
            "MonsoonIntensity",
            "TopographyDrainage",
            "RiverManagement",
            "Deforestation",
            "Urbanization",
            "ClimateChange",
            "DamsQuality",
            "Siltation",
            "AgriculturalPractices",
            "Encroachments",
            "IneffectiveDisasterPreparedness",
            "DrainageSystems",
            "CoastalVulnerability",
            "Landslides",
            "Watersheds",
            "DeterioratingInfrastructure",
            "PopulationScore",
            "WetlandLoss",
            "InadequatePlanning",
            "PoliticalFactors"
        ]

        sample = pd.DataFrame(data, columns=columns)

        prediction = model.predict(sample)[0]

        if prediction < 0.30:
            risk = "🟢 Low Flood Risk"
        elif prediction < 0.60:
            risk = "🟡 Moderate Flood Risk"
        else:
            risk = "🔴 High Flood Risk"

        percentage = round(prediction * 100, 1)

        return render_template(
            "result.html",
            prediction=round(prediction, 3),
            percentage=percentage,
            risk=risk   
        )

    return render_template("predict.html")


if __name__ == "__main__":
    app.run(debug=True)