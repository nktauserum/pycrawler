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
            print(f"New request with URLs {request.url}")
            responses = []
            with futures.ThreadPoolExecutor(max_workers=20) as executor:
                future_results = [executor.submit(extract, url) for url in request.url]
                for future in futures.as_completed(future_results):
                    result = future.result()
                    if result is not None:
                        responses.append(service_pb2.ExtractResponse(
                            url=result.url,
                            title=result.title,
                            sitename=result.sitename,
                            text=result.text
                        ))
            return service_pb2.ExtractResponses(responses=responses)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return service_pb2.ExtractResponses()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ExtractServiceServicer_to_server(
        ExtractServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()
