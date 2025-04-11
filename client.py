import grpc
import task_pb2
import task_pb2_grpc
from flask import Flask, request, jsonify

app = Flask(__name__)

# Create a channel which is a address to the server
CHANNEL = grpc.insecure_channel('localhost:50051')

# Creating a proxy that acts as authorize entity to interact with remote services over the network
stub = task_pb2_grpc.TaskServiceStub(channel=CHANNEL)


@app.route('/create-task', methods=["POST"])
def create_task():
    data = request.get_json()
    # Serializing the task into a protbuf
    gprc_request = task_pb2.CreateTaskRequest(
        task_id = data.get("task_id", ""),
        name = data.get("task_name", ""),
        status = data.get("status", "pending")
    )

    try:
        response = stub.CreateTask(gprc_request)
        print(f"Resonse from the server - {response.success}")
        return jsonify({
            "message": response.message,
            "success": response.success
        }), 200
    except grpc.RpcError as e:
        print(f"Error occured while creating task - {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500




if __name__ == "__main__":
    print("Client Server running...")
    app.run(debug=True)
