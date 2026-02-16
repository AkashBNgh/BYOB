import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from nlp_engine import natural_language_to_sql
from db_manager import execute_query
from visualizer import create_plot

load_dotenv()

# Initialize Slack App
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

# ---------------- USE CASE 1: QUERY ----------------
@app.message("query:")
def handle_query(message, say):
    user_text = message["text"].replace("query:", "").strip()
    say(f"🔍 Processing query: {user_text}...")

    try:
        # 1. NLP → SQL
        sql = natural_language_to_sql(user_text)
        print(f"Generated SQL: {sql}")

        # 2. Execute SQL
        result_df = execute_query(sql)

        # 3. Respond
        if result_df.empty:
            say("No data found for that query.")
        else:
            table = result_df.to_string(index=False)
            say(f"Here are the results:\n```{table}```")

    except Exception as e:
        say(f"❌ Error: {e}")

# ---------------- USE CASE 2: PLOT ----------------
@app.message("plot:")
def handle_plot(message, say, client):
    user_text = message["text"].replace("plot:", "").strip()
    say(f"📊 Generating graph for: {user_text}...")

    try:
        # 1. NLP → SQL
        sql = natural_language_to_sql(user_text)

        # 2. Execute SQL
        result_df = execute_query(sql)

        if result_df.empty:
            say("No data available to plot.")
            return

        # 3. Create plot
        image_file = create_plot(result_df, title=user_text)

        if image_file:
            client.files_upload_v2(
                channel=message["channel"],
                file=image_file,
                title="Generated Graph",
                initial_comment="Here is your requested graph 📈"
            )
        else:
            say("Could not generate plot.")

    except Exception as e:
        say(f"❌ Error: {e}")

# ---------------- START BOT ----------------
if __name__ == "__main__":
    SocketModeHandler(
        app,
        os.getenv("SLACK_APP_TOKEN")  # MUST be xapp-
    ).start()
