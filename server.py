
import grpc
from concurrent import futures
import json
from tools import service_pb2
from tools import service_pb2_grpc
from parse import extract
from timing import timing

class ExtractServiceServicer(service_pb2_grpc.ExtractServiceServicer):
    @timing
    def Extract(self, request, context):
        try:
            print(f"New request with URL {request.url}")
            result = extract(request.url)
            return service_pb2.ExtractResponse(title=result.title, sitename=result.sitename, text=result.text)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return service_pb2.ExtractResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ExtractServiceServicer_to_server(
        ExtractServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
