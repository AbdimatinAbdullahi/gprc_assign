from flask import Flask
import grpc
import task_pb2
import task_pb2_grpc
from concurrent import futures

tasks = {}

# Create a TaskService class that implements rpc service that is defined in proto file
# By inheriting the service taskserviceservicer, you are fullfing the requiremenst to implement the rpc methods that is defined in service
class TaskService(task_pb2_grpc.TaskServiceServicer):
    def CreateTask(self, request, context):
        print("Request has hit here ...")
        task_id = request.task_id
        if task_id in tasks:
            return task_pb2.TaskResponse(
                message=f"Task with task id already exists",
                success=False
            )
        
        tasks[task_id] = {
            "name" : request.name,
            "status" : request.status
        }

        print(f"Task created: {tasks[task_id]}")

        return task_pb2.TaskResponse(
            message=f"Task create successfully",
            success=True
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2)) # Creating an instance of grpc server
    task_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server running at port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()