from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from helpers.connect_db import DBConnect

# INIT APP
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# INIT DB ONCE
db = DBConnect()
db.connect()
print("✅ Database connected successfully.")


# ROUTES
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/tables")
def manage_tables():
    rows = db.query_db("SELECT * FROM `table`")
    return render_template("manage_tables.html", tables=rows)


@app.route("/tables/add", methods=["POST"])
def add_table():
    position = request.form.get("position")
    capacity = request.form.get("capacity")
    maintenance_flag = int(request.form.get("maintenance_flag", 0))
    special_event_flag = int(request.form.get("special_event_flag", 0))
    q = "INSERT INTO `table` (position, capacity, active_flag, maintenance_flag, special_event_flag) VALUES (%s, %s, 1, %s, %s)"
    db.execute_query(q, (position, capacity, maintenance_flag, special_event_flag))
    return redirect(url_for("manage_tables"))


@app.route("/book", methods=["GET", "POST"])
def book_table():
    if request.method == "POST":
        customer_name = request.form.get("customer_name")
        customer_email = request.form.get("customer_email")
        party_size = int(request.form.get("party_size"))
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")

        # Find customer or create
        customer = db.query_db(
            "SELECT id FROM customer WHERE name=%s AND email=%s",
            (customer_name, customer_email),
            one=True,
        )
        if not customer:
            db.execute_query(
                "INSERT INTO customer (name, email) VALUES (%s, %s)",
                (customer_name, customer_email),
            )
            customer = db.query_db(
                "SELECT id FROM customer WHERE name=%s AND email=%s",
                (customer_name, customer_email),
                one=True,
            )
        customer_id = customer["id"]

        # Find available tables (not in maintenance/special event, not double-booked)
        available_tables = db.query_db(
            """
            SELECT * FROM `table` WHERE active_flag=1 AND maintenance_flag=0 AND special_event_flag=0 AND capacity >= %s
            AND id NOT IN (
                SELECT table_id FROM booking WHERE NOT (end_time <= %s OR start_time >= %s) AND active_flag=1
            )
            ORDER BY capacity ASC
            """,
            (party_size, start_time, end_time),
        )

        assigned_table_id = None
        if available_tables:
            # Assign smallest suitable table
            assigned_table_id = available_tables[0]["id"]
        else:
            # Try to combine tables for large group
            tables = db.query_db(
                "SELECT * FROM `table` WHERE active_flag=1 AND maintenance_flag=0 AND special_event_flag=0"
            )
            from itertools import combinations

            found = False
            for r in range(2, len(tables) + 1):
                for combo in combinations(tables, r):
                    total_capacity = sum(t["capacity"] for t in combo)
                    ids = [t["id"] for t in combo]
                    # Check if all tables are free for the slot
                    conflict = db.query_db(
                        "SELECT * FROM booking WHERE table_id IN (%s) AND NOT (end_time <= %s OR start_time >= %s) AND active_flag=1"
                        % (",".join(map(str, ids)), start_time, end_time)
                    )
                    if total_capacity >= party_size and not conflict:
                        assigned_table_id = ids[
                            0
                        ]  # For simplicity, assign first table (extend for multi-table booking)
                        found = True
                        break
                if found:
                    break
        if not assigned_table_id:
            # Overbooking risk: allow booking but warn (could be extended)
            return (
                "No available tables for the requested time/size. Overbooking not allowed.",
                409,
            )

        # Insert booking
        db.execute_query(
            "INSERT INTO booking (table_id, customer_id, start_time, end_time, active_flag) VALUES (%s, %s, %s, %s, 1)",
            (assigned_table_id, customer_id, start_time, end_time),
        )
        return redirect(url_for("book_table"))
    return render_template("book_table.html")


@app.route("/report")
def report():
    rows = db.query_db(
        """
        SELECT b.*, t.position, t.capacity 
        FROM `booking` b 
        JOIN `table` t ON b.table_id = t.id 
        ORDER BY start_time DESC
    """
    )
    return render_template("report.html", bookings=rows)


# API endpoints
@app.route("/api/tables")
def api_tables():
    data = db.query_db("SELECT * FROM `table`")
    return jsonify(data)


@app.route("/api/bookings")
def api_bookings():
    data = db.query_db("SELECT * FROM `booking`")
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5046, debug=True)
