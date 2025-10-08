import azure.functions as func
from azure.cosmos import CosmosClient
import json

class Function1:
    def __init__(self, logger, cosmos_client):
        self.logger = logger
        self.cosmos_client = cosmos_client

    def run(self, req: func.HttpRequest) -> func.HttpResponse:
        self.logger.info('Python HTTP trigger function processed a request.')

        id = req.params.get('id')
        if not id:
            return func.HttpResponse("ID não fornecido", status_code=400)

        container = self.cosmos_client.get_container_client("DioFlixDB", "movies")
        query = f"SELECT * FROM c WHERE c.id = @id"
        params = {"@id": id}
        results = list(container.query_items(query=query, parameters=params))

        if not results:
            return func.HttpResponse("Nenhum filme encontrado", status_code=404)

        return func.HttpResponse(json.dumps(results[0]), status_code=200, headers={"Content-Type": "application/json"})

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logger = func.get_logger()
    cosmos_client = CosmosClient(os.environ["CosmosDBConnectionString"])
    function1 = Function1(logger, cosmos_client)
    return function1.run(req)
