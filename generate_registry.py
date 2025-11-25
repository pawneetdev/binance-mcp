from adapter import (
    OpenAPILoader,
    Normalizer,
    ToolGenerator,
    ToolRegistry,
    APIExecutor,
    BearerAuth,
    MCPServer
)
import json
import logging
import sys

loader = OpenAPILoader()
spec = loader.load("https://raw.githubusercontent.com/binance/binance-api-swagger/refs/heads/master/spot_api.yaml")

normalizer = Normalizer()
endpoints = normalizer.normalize_openapi(spec)

generator = ToolGenerator(api_name="binance_spot_api")
tools = generator.generate_tools(endpoints)

registry = ToolRegistry(name="Binance Spot API")
registry.add_tools(tools)

registry_file = "binance_spot_toolkit.json"
registry.export_json(registry_file)

endpoints_data = [endpoint.model_dump() for endpoint in endpoints]

endpoints_file = "binance_spot_endpoints.json"

with open(endpoints_file, "w") as f:
    json.dump(endpoints_data, f, indent=2)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

logger.info("=" * 70)
logger.info("Registry generation completed!")
logger.info(f"  Tools: {len(tools)}")
logger.info(f"  Endpoints: {len(endpoints)}")
logger.info(f"  Registry file: {registry_file}")
logger.info(f"  Endpoints file: {endpoints_file}")
logger.info("=" * 70)
