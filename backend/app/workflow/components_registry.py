COMPONENT_DEFINITIONS = [
    {
        "type": "userQuery",
        "name": "User Query",
        "description": "Starting point of the workflow. Accepts user input.",
        "ui_schema": {"fields": []},
        # Updated: Handles for all 4 directions (Source & Target)
        "handles": [
            {"id": "top-source", "type": "source", "position": "top"},
            {"id": "top-target", "type": "target", "position": "top"},
            {"id": "right-source", "type": "source", "position": "right"},
            {"id": "right-target", "type": "target", "position": "right"},
            {"id": "bottom-source", "type": "source", "position": "bottom"},
            {"id": "bottom-target", "type": "target", "position": "bottom"},
            {"id": "left-source", "type": "source", "position": "left"},
            {"id": "left-target", "type": "target", "position": "left"}
        ],
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
                    "default": "gpt-4",
                },
                {
                    "name": "temperature",
                    "label": "Temperature",
                    "type": "number",
                    "min": 0,
                    "max": 1,
                    "step": 0.1,
                    "default": 0.7,
                },
                {
                    "name": "system_prompt",
                    "label": "System Prompt",
                    "type": "textarea",
                    "default": "",
                },
            ]
        },
        # Updated: Handles for all 4 directions (Source & Target)
        "handles": [
            {"id": "top-source", "type": "source", "position": "top"},
            {"id": "top-target", "type": "target", "position": "top"},
            {"id": "right-source", "type": "source", "position": "right"},
            {"id": "right-target", "type": "target", "position": "right"},
            {"id": "bottom-source", "type": "source", "position": "bottom"},
            {"id": "bottom-target", "type": "target", "position": "bottom"},
            {"id": "left-source", "type": "source", "position": "left"},
            {"id": "left-target", "type": "target", "position": "left"}
        ],
    },
    {
        "type": "knowledgeBase",
        "name": "Knowledge Base",
        "description": "Retrieves relevant documents from vector store",
        "ui_schema": {
            "fields": [
                # NEW FIELD: File Upload
                {
                    "name": "knowledge_doc",
                    "label": "Upload Document",
                    "type": "file", 
                    "description": "Upload PDF or TXT to index",
                },
                {
                    "name": "top_k",
                    "label": "Top K Results",
                    "type": "number",
                    "default": 5,
                },
                {
                    "name": "score_threshold",
                    "label": "Score Threshold",
                    "type": "number",
                    "default": 0.75,
                },
            ]
        },
        # Updated: Handles for all 4 directions (Source & Target)
        "handles": [
            {"id": "top-source", "type": "source", "position": "top"},
            {"id": "top-target", "type": "target", "position": "top"},
            {"id": "right-source", "type": "source", "position": "right"},
            {"id": "right-target", "type": "target", "position": "right"},
            {"id": "bottom-source", "type": "source", "position": "bottom"},
            {"id": "bottom-target", "type": "target", "position": "bottom"},
            {"id": "left-source", "type": "source", "position": "left"},
            {"id": "left-target", "type": "target", "position": "left"}
        ],
    },
    {
        "type": "output",
        "name": "Output",
        "description": "Final output of the workflow",
        "ui_schema": {"fields": []},
        # Updated: Handles for all 4 directions (Source & Target)
        "handles": [
            {"id": "top-source", "type": "source", "position": "top"},
            {"id": "top-target", "type": "target", "position": "top"},
            {"id": "right-source", "type": "source", "position": "right"},
            {"id": "right-target", "type": "target", "position": "right"},
            {"id": "bottom-source", "type": "source", "position": "bottom"},
            {"id": "bottom-target", "type": "target", "position": "bottom"},
            {"id": "left-source", "type": "source", "position": "left"},
            {"id": "left-target", "type": "target", "position": "left"}
        ],
    },
]