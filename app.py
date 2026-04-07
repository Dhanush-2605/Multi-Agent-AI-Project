from flask import Flask, render_template, request, jsonify
# Import your Crew and Tasks from your existing files!
from crewai import Crew, Process
from agents import miss_minutes, ouroboros, agent_mobius
from tasks import fact_check_task, simulate_branch_task, judge_task

app = Flask(__name__)

@app.route('/')
def home():
    # Serves the HTML file we just made
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # 1. Catch the user's theory from the webpage
    data = request.json
    theory_input = data.get('theory')

    print(f"🔭 TVA Monitor received Nexus Event: {theory_input}")

    # 2. Dynamically update the task descriptions with the user's new input!
    # fact_check_task.description = f"Conduct a thorough factual investigation of this scenario: '{theory_input}'..."
    # simulate_branch_task.description = f"Simulate the temporal ripple effect for: '{theory_input}'..."
    # judge_task.description = f"Review the theory: '{theory_input}'. Draft a Pruning Report and state if it is an Anomaly or a Stable Branch."

    # 3. Assemble and run the Crew
    tva_crew = Crew(
        agents=[miss_minutes, ouroboros, agent_mobius],
        tasks=[fact_check_task, simulate_branch_task, judge_task],
        process=Process.sequential,
        max_rpm=2
    )

    # Kickoff the agents
    result = tva_crew.kickoff(inputs={'fan_theory_input': theory_input})
    # 4. Send Mobius's final report back to the website
    # CrewAI kickoff returns an object, so we cast it to a string
    return jsonify({"report": str(result)})

if __name__ == '__main__':
    # Starts the web server
    app.run(debug=True, port=5000)