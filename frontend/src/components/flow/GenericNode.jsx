import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';
import { MessageSquare, Database, Sparkles, FileText } from 'lucide-react';
import { NodeFieldRenderer } from './NodeFieldRenderer';

const ICONS = {
  userQuery: MessageSquare,
  knowledgeBase: Database,
  llm: Sparkles,
  output: FileText,
};

/* ---------- HANDLE TOPOLOGY (FIX #008) ---------- */
const HANDLE_CONFIG = {
  userQuery: [
    { type: 'source', position: Position.Bottom, id: 'query' }
  ],

  knowledgeBase: [
    { type: 'source', position: Position.Bottom, id: 'context' }
  ],

  llm: [
    { type: 'target', position: Position.Top, id: 'query' },
    { type: 'target', position: Position.Top, id: 'context' },
    { type: 'source', position: Position.Bottom, id: 'output' }
  ],

  output: [
    { type: 'target', position: Position.Top, id: 'output' }
  ]
};



const GenericNode = ({ id, data }) => {
  const Icon = ICONS[data.type] || MessageSquare;
  console.log("Node data:", data);
  const uiSchema =data.ui_schema;

  const handles = HANDLE_CONFIG[data.type] || [];

  const handleChange = (name, value) => {
    data.onChange(id, { [name]: value });
  };

  return (
    <div className="bg-white border rounded p-4 w-64 shadow-sm">
      {handles.map((h) => (
        <Handle
          key={h.id}
          type={h.type}
          position={h.position}
          id={h.id}
        />
      ))}

      <div className="flex items-center gap-2 mb-2">
        <Icon size={14} />
        <strong className="text-sm">{data.label}</strong>
      </div>

      <p className="text-xs text-gray-500 mb-2">
        {data.description}
      </p>

      {uiSchema.fields.map((f) => (
        <NodeFieldRenderer
          key={f.name}
          field={f}
          value={data.values?.[f.name]}
          onChange={handleChange}
        />
      ))}
    </div>
  );
};

export default memo(GenericNode);
