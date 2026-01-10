COMPONENT_DEFINITIONS = [
    {
        "type": "userQuery",
        "name": "User Query",
        "description": "Starting point of the workflow. Accepts user input.",
        "ui_schema": {
            "fields": []
        }
    },
    {
        "type": "llm",
        "name": "LLM",
        "description": "Large Language Model node",
        "ui_schema": {
            "fields": [
                {
                    "name": "model",
                    "label": "Model",
                    "type": "select",
                    "options": ["gpt-4", "gpt-3.5-turbo"],
                    "default": "gpt-4"
                },
                {
                    "name": "temperature",
                    "label": "Temperature",
                    "type": "number",
                    "min": 0,
                    "max": 1,
                    "step": 0.1,
                    "default": 0.7
                },
                {
                    "name": "system_prompt",
                    "label": "System Prompt",
                    "type": "textarea",
                    "default": ""
                }
            ]
        }
    },
    {
        "type": "knowledgeBase",
        "name": "Knowledge Base",
        "description": "Retrieves relevant documents from vector store",
        "ui_schema": {
            "fields": [
                {
                    "name": "top_k",
                    "label": "Top K Results",
                    "type": "number",
                    "default": 5
                },
                {
                    "name": "score_threshold",
                    "label": "Score Threshold",
                    "type": "number",
                    "default": 0.75
                }
            ]
        }
    },
    {
        "type": "output",
        "name": "Output",
        "description": "Final output of the workflow",
        "ui_schema": {
            "fields": []
        }
    }
]
