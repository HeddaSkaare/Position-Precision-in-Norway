import json
import os
from flask import Flask, Response, jsonify, request, stream_with_context
from computebaner import  get_gnss, getDayNumber, runData_check_sight
from computeDOP import best, find_dop_on_point
from flask_cors import CORS
from datetime import datetime
from romsdalenRoad import calculate_travel_time, connect_total_road_segments, get_road_api
import rasterio
import psutil, os
import threading
import uuid
import traceback
distance = None
points = None
port = int(os.environ.get("PORT", 5000))

app = Flask(__name__)
# CORS(app, resources={r"/satellites": {"origins": "http://localhost:3000"}}, supports_credentials=True)
# CORS(app, resources={r"/dopvalues": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/*": {
    "origins": [
        "http://localhost:3000",
        "https://master-2025.vercel.app"
    ],
    "supports_credentials": True
}})

# @app.route('/satellites', methods=['POST', 'OPTIONS'])
# def satellites():
#     if request.method == 'OPTIONS':
#         # Handle the preflight request with necessary headers
#         response = jsonify({'status': 'Preflight request passed'})
#         response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
#         response.headers.add("Access-Control-Allow-Headers", "Content-Type")
#         response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
#         return response, 200

#     # Main POST request handling
#     data = request.json  
#     time = data.get('time').strip('Z')
#     elevation_angle = data.get('elevationAngle')
#     gnss = data.get('GNSS')
#     epoch = data.get('epoch')
#     frequency = int(data.get('epochFrequency'))
#     point = data.get('point')
#     #print(f'point: {point}')
    
#     is_processing = True
#     list, df,elevation_cutoffs, obs_cartesian = runData_check_sight(gnss, elevation_angle, time, epoch,frequency, point) 
#     elevation_strings = [str(elevation) for elevation in elevation_cutoffs]
#     DOPvalues = best(df, obs_cartesian)

#     is_processing = False
    
#     if not is_processing:
#         response = jsonify({'message': 'Data processed successfully', 'data': list, 'DOP': DOPvalues,   'elevation_cutoffs': elevation_strings})
#         response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*")) 
#         return response, 200
#     else:
#         response = jsonify({"data": "Data is not ready"})
#         response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
#         return response, 202
jobs = {}

@app.route('/satellites', methods=['POST'])
def satellites():
    data = request.json
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending", "result": None}

    thread = threading.Thread(target=process_satellite_job, args=(job_id, data))
    thread.start()

    response = jsonify({"job_id": job_id})
    origin = request.headers.get("Origin", "*")
    response.headers.add("Access-Control-Allow-Origin", origin)
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response, 202

def process_satellite_job(job_id, data):
    try:
        # Bruk data['time'], data['GNSS'], osv. her
        list, df, elevation_cutoffs, obs_cartesian = runData_check_sight(
            data['GNSS'], data['elevationAngle'], data['time'].strip('Z'),
            data['epoch'], int(data['epochFrequency']), data['point']
        )
        DOPvalues = best(df, obs_cartesian)
        jobs[job_id]["status"] = "done"
        jobs[job_id]["result"] = {
            "list": list,
            "elevation_cutoffs": [str(e) for e in elevation_cutoffs],
            "DOP": DOPvalues
        }
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["result"] = {"error": str(e)}

@app.route('/job-status/<job_id>', methods=['GET'])
def job_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    return jsonify({
        "status": job["status"],
        "progress": job.get("progress", 0)
    })


@app.route('/job-result/<job_id>', methods=['GET'])
def job_result(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    if job["status"] != "done":
        return jsonify({"error": "Job not ready"}), 202
    return jsonify(job["result"])

@app.route('/road', methods=['POST'])
def road():
    data = request.get_json()
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "pending",
        "progress": 0,
        "result": None,
        "type": "road"
    }

    thread = threading.Thread(target=process_road_job, args=(job_id, data))
    thread.start()

    return jsonify({"job_id": job_id}), 202

def process_road_job(job_id, data):
    try:
        vegReferanse = data.get('vegReferanse')
        startPoint = data.get('startPoint')
        endPoint = data.get('endPoint')
        distance = data.get('distance')

        if not vegReferanse or not startPoint or not endPoint or not distance:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["result"] = {
                'error': 'Missing input parameters.',
                'message': 'Please provide startPoint, endPoint, distance and vegReferanse.'
            }
            return

        jobs[job_id]["progress"] = 10  # optional progress feedback

        segmenter, df, vegsystemreferanse= get_road_api(startPoint, endPoint, vegReferanse)
        jobs[job_id]["progress"] = 50
        road_utm, road_wgs = connect_total_road_segments(segmenter,df, vegsystemreferanse, startPoint, endPoint)
        jobs[job_id]["progress"] = 75
        points = calculate_travel_time(road_utm, float(distance))
        jobs[job_id]["progress"] = 90

        jobs[job_id]["status"] = "done"
        jobs[job_id]["result"] = {
            'message': 'Data processed successfully',
            'road': road_wgs,
            'points': points
        }
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        jobs[job_id]["status"] = "error"
        jobs[job_id]["result"] = {
            'error': 'Unexpected error',
            'details': str(e),
            'message': 'An unexpected error occurred. Please try again later.'
        }

# @app.route('/road', methods=['POST', 'OPTIONS'])
# def road():
#     if request.method == 'OPTIONS':
#         # Handle the preflight request (CORS preflight)
#         response = jsonify({'status': 'Preflight request passed'})
#         response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
#         response.headers.add("Access-Control-Allow-Headers", "Content-Type")
#         response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
#         return response, 200

#     try:
#         vegReferanse = request.json.get('vegReferanse')
#         startPoint = request.json.get('startPoint')
#         endPoint = request.json.get('endPoint')
#         distance = request.json.get('distance')

#         # Validate input
#         if not vegReferanse or not startPoint or not endPoint or not distance:
#             response = jsonify({'error': 'Missing input parameters.', 'message': 'Please provide startPoint, endPoint, distance and vegReferanse.'})
#             response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
#             return response, 400

#         # Get road data
#         road_utm, road_wgs = get_road_api(startPoint, endPoint, vegReferanse)

#         # Calculate points
#         points = calculate_travel_time(road_utm, float(distance))

#         response = jsonify({'message': 'Data processed successfully', 'road': road_wgs, 'points': points})
#         response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
#         return response, 200

#     except IndexError as e:
#         response = jsonify({
#             'error': 'No road data found for the given input.',
#             'details': str(e),
#             'message': 'The road couldn’t be found. Please check all the input parameters and be more specific with the start and end markers.'
#         })
#         response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
#         return response, 400

#     except Exception as e:
#         # Log full error in backend
#         print(traceback.format_exc())
#         response = jsonify({
#             'error': 'An unexpected error occurred.',
#             'details': str(e),
#             'message': 'An unexpected error occurred. Please try again later.'
#         })
#         response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
#         return response, 500

@app.route('/dopvalues', methods=['POST'])
def dopvalues():
    data = request.get_json()
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending", "result": None}

    thread = threading.Thread(target=process_dopvalues_job, args=(job_id, data))
    thread.start()

    return jsonify({"job_id": job_id}), 202

def process_dopvalues_job(job_id, data):
    try:
        time_str = data.get('time').strip('Z')
        elevation_angle = data.get('elevationAngle')
        gnss = data.get('GNSS')
        points = data.get('points')
        
        time = datetime.fromisoformat(time_str)
        daynumber = getDayNumber(time)
        gnss_mapping = get_gnss(daynumber, time.year)

        raster_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "merged_raster.tif")
        dop_list = []

        with rasterio.open(raster_path) as src:
            dem_data = src.read(1)
            total_steps = len(points)
            for step, point in enumerate(points, start=1):
                dop_point = find_dop_on_point(dem_data, src, gnss_mapping, gnss, time, point, elevation_angle, step)
                dop_list.append(dop_point)
                progress = int((step / total_steps) * 100)
                jobs[job_id]["progress"] = progress  # 💡 Progress-tracking

        jobs[job_id]["status"] = "done"
        jobs[job_id]["result"] = {"dopvalues": dop_list}
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["result"] = {"error": str(e)}
  
    
# @app.route('/dopvalues', methods=['POST', 'OPTIONS'])
# def dopValues():
#     if request.method == 'OPTIONS':
#         return jsonify({'status': 'Preflight request passed'}), 200

#     try:
#         data = request.get_json()
#         time_str = data.get('time').strip('Z')
#         elevation_angle = data.get('elevationAngle')
#         gnss = data.get('GNSS')
#         points = data.get('points')
#     except Exception as e:
#         return jsonify({"error": f"Invalid data format: {e}"}), 400

#     time = datetime.fromisoformat(time_str)
#     daynumber = getDayNumber(time)
#     gnss_mapping = get_gnss(daynumber, time.year)
#     total_steps = len(points)

#     CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
#     raster_path = os.path.join(CURRENT_DIR, "data", "merged_raster.tif")

#     def generate():
#         # 🔁 Umiddelbar kontakt
#         yield "0\n\n"

#         dop_list = []
#         with rasterio.open(raster_path) as src:
#             dem_data = src.read(1)

#             for step, point in enumerate(points, start=1):
#                 dop_point = find_dop_on_point(dem_data, src, gnss_mapping, gnss, time, point, elevation_angle, step)
#                 dop_list.append(dop_point)
#                 yield f"{int((step / total_steps) * 100)}\n\n"

#         yield f"{json.dumps(dop_list)}\n\n"

#     response = Response(stream_with_context(generate()), content_type='text/event-stream')
#     response.headers["Access-Control-Allow-Origin"] = "https://master-2025.vercel.app"
#     response.headers["Access-Control-Allow-Credentials"] = "true"
#     return response



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=port, debug=True)