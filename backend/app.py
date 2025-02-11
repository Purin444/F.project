from flask import Flask, request, render_template
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv  # สำหรับโหลด .env
from backend.extensions import mongo, cors
from backend.routes.holiday_routes import holiday_bp
from backend.routes.user_routes import user_bp
from backend.routes.attendance_routes import attendance_bp
from backend.routes.ot_request_routes import ot_request_bp
from backend.routes.auth_routes import auth_bp
from backend.routes.salary_routes import salary_bp
from backend.routes.department_routes import department_bp
from backend.routes.ot_request_routes import accepted_ot_bp

# โหลดค่าจากไฟล์ .env
load_dotenv()

app = Flask(__name__)

# **แก้ไข**: ใช้ Environment Variable สำหรับ MongoDB URI
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/time_attendance_db")
app.config["JSONIFY_MIMETYPE"] = "application/json"
app.config["JSON_SORT_KEYS"] = False

# เปิดใช้งาน Mongo และ CORS
mongo.init_app(app)
cors.init_app(app)
CORS(app)

# ตั้งค่า Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ลงทะเบียน Blueprints
app.register_blueprint(holiday_bp)
app.register_blueprint(user_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(ot_request_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(salary_bp)
app.register_blueprint(department_bp)
app.register_blueprint(accepted_ot_bp)

# Middleware สำหรับ Logging
@app.before_request
def before_request_logging():
    logger.info(f"Incoming request: {request.method} {request.path}")

# Root Path
@app.route('/', methods=['GET'])
def home():
    return render_template('auth.html')

# Health Check
@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "ok"}, 200

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return {"error": "Resource not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal server error"}, 500

# **แก้ไข**: เพิ่มเงื่อนไขเพื่อรองรับการ Deploy บน Gunicorn
if __name__ == '__main__':
    logger.info("Application is starting in development mode...")
    app.run(debug=True, host='0.0.0.0', port=5001)
