from agent import graph
from dotenv import load_dotenv

load_dotenv()
input_data = {
    "project_name": "react",
    "github_url": "https://github.com/facebook/react",
    "readme": "React is a library for building user interfaces.",
}

result = graph.invoke(input_data)

print(result)