import numpy as np
from app import app
from app.db import get_database_connection
from flask import render_template
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64


@app.route('/', methods=['GET'])
def get_home():
    title = "CS532 NOSQL DATA ANALYSIS PROJECT"
    return render_template("home.html", title=title)

@app.route('/data_analysis_one', methods=['GET'])
def analysis_one():
    collection = get_database_connection()

    name = "Wayne Rooney"
    # club = ["F.C. Barcelona", "FC Barcelona"]
    pipeline = [
        {
            "$match": {
                "Name": name, 
                # "Club": {"$in":club},
                "Club": "Manchester United",
                "$or": [
                    {"PlayedYear": { "$gte": 2012, "$lte": 2021 }},
                    # {"Played_Year": 2014},
                ] 
            }
        },
        {
            "$group": {
                "_id": {
                    "Played_Year": "$Played_Year",
                    "Club_Position": "$Club_Position"
                },
                "AvgOverall": { "$avg": "$Overal" }       
            }
        },
        {
            "$project": {
                "_id": 0, 
                "Played_Year": "$_id.Played_Year",
                "PlayedYear": "$_id.PlayedYear",
                "Club_Position": "$_id.Club_Position",
                "AvgOverall": 1
            }
        }
    ]
    data = list(collection.aggregate(pipeline))
    print(data)

    positions = [entry["Club_Position"] for entry in data]
    avg_overall_values = [entry["AvgOverall"] for entry in data]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(positions, avg_overall_values, color='skyblue')
    plt.xlabel('Club Position')
    plt.ylabel('Overall Performance Metric')
    plt.title(f'Performance w.r.t club positions of {name}')
    plt.xticks(rotation=45)
    plt.tight_layout()

    for bar, value in zip(bars, avg_overall_values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), round(value, 2),
                ha='center', va='bottom', color='black', fontsize=9, fontweight='bold')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    title = "Analysis Task 1: How player performed in the last decade with respect to their playing position for the club."

    return render_template('plot.html', title=title, plot_url=plot_url)
    # return json.loads(json_util.dumps(data))


@app.route('/data_analysis_two')
def analysis_two():
    collection = get_database_connection()

    age_min = 20
    age_max = 35

    pipeline = [
    {
        "$match": {
            "Nation": { "$in": ["Spain", "Argentina", "Portugal", "Brazil"] },
            "Age": { "$gte": age_min, "$lte": age_max }
        }
    },
    {
        "$group": {
            "_id": {
                "Nation": "$Nation"
            },
            "maxPlayerData": {
                "$max": {
                    "Strength": "$Strength",
                    "Stamina": "$Stamina",
                    "Acceleration": "$Acceleration",
                    "combinedValue": {
                        "$sum": ["$Strength", "$Stamina", "$Acceleration"]
                    },
                    "Name": "$Name",
                    "Nation": "$Nation"
                }
            }
        }
    },
    {
        "$project": { "_id": 0, "maxPlayerData": 1 }
    },
    {
        "$replaceRoot": { "newRoot": "$maxPlayerData" }
    }
]

    data = list(collection.aggregate(pipeline))
    print(data)

    nations = [item['Nation'] for item in data]
    max_players = [item['combinedValue'] for item in data]

    plt.figure(figsize=(16, 6))
    bars = plt.barh(nations, max_players, color='skyblue')
    plt.xlabel('Maximum Physical Performance Metric')
    plt.title(f'Player performance by Nation who belong to age group ({age_min}-{age_max})')

    for bar, player_name in zip(bars, [item['Name'] for item in data]):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, player_name, ha='left', va='center')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    title="Data Analysis 2: Analysis of player with highest physical performance grouped by age group and nationality and how they compare with each other."

    return render_template('plot.html', title=title, plot_url=plot_url)



@app.route('/data_analysis_three', methods=['GET'])
def analysis_three():
    collection = get_database_connection()

    # clubs = ["F.C. Barcelona", "FC Barcelona"]
    clubs = ["Arsenal"]

    pipeline = [
    {
        "$match": {
            "Club": {"$in": clubs},
            "Club_Position": {"$in": ["ST", "LCM"]}
        }
    },
    {
        "$group": {
            "_id": {
                "Preferred_Foot": "$PreferredFoot",
                "Club_Position": "$Club_Position"
            },
            "sumPassVision": {
                "$sum": {
                    "$sum": ["$longPass", "$shortPass", "$Vision"]
                }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "PreferredFoot": "$_id.Preferred_Foot",
            "Club_Position": "$_id.Club_Position",
            "PassVision": {
                "$avg": "$sumPassVision"
            }
        }
    }
]


    data = list(collection.aggregate(pipeline))
    print(data)

    if not data:
        return render_template('plot.html')

    positions = list(set(item['Club_Position'] for item in data))
    positions.sort() 
    ball_control_R = [item['PassVision'] for item in data if item['PreferredFoot'] == 'R']
    ball_control_L = [item['PassVision'] for item in data if item['PreferredFoot'] == 'L']

    x = np.arange(len(positions))

    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    plt.bar(x - bar_width/2, ball_control_R, bar_width, label='Preferred Foot: R')
    plt.bar(x + bar_width/2, ball_control_L, bar_width, label='Preferred Foot: L')

    plt.xlabel('Club Positions')
    plt.ylabel('Ball Control Performance')
    plt.title('Ball Control Performance Analysis by Club Positions w.r.t Preferred Foot')
    plt.xticks(x, positions)
    plt.legend()
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    title="Data Analysis 3: Analysis of left footed and right footed player's ball control metrics - long pass, short pass and vision w.r.t their positions for the club"

    return render_template('plot.html', title=title, plot_url=plot_url)