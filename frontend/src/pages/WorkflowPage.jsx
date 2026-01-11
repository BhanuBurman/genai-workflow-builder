import React from "react";
import { ReactFlowProvider } from "reactflow";
import WorkflowBuilder from "../components/WorkflowBuilder";
import { MessageCircleMore, Play } from "lucide-react";

export default function WorkflowPage() {
  return (
    <>
      <ReactFlowProvider>
        <WorkflowBuilder />
      </ReactFlowProvider>
    </>
  );
}
