from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        players = [
            request.form["p1"],
            request.form["p2"],
            request.form["p3"],
            request.form["p4"]
        ]
        rounds = int(request.form["rounds"])
        return render_template("scores.html", players=players, rounds=rounds)
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    players = request.form.getlist("players")
    rounds = int(request.form["rounds"])

    totals = {p: 0.0 for p in players}
    all_data = []

    for r in range(rounds):
        round_info = {"round": r + 1, "players": {}}
        for p in players:
            call = request.form[f"{p}_call_{r}"]
            result = float(request.form[f"{p}_result_{r}"])
            totals[p] += result
            round_info["players"][p] = {
                "call": call,
                "result": result
            }
        all_data.append(round_info)

    max_score = max(totals.values())
    winners = [p for p, s in totals.items() if s == max_score]

    return render_template(
        "result.html",
        totals=totals,
        winners=winners,
        all_data=all_data
    )


if __name__ == "__main__":
    app.run()
    
