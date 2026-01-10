import React, { useEffect, useState } from 'react';
import { MessageSquare, Database, Sparkles, FileText, Loader2 } from 'lucide-react';
import { componentService } from '../../services/componentService'; // Import your service

const ICON_MAP = {
  userQuery: MessageSquare,
  knowledgeBase: Database,
  llm: Sparkles,
  output: FileText
};

export default function Sidebar() {
  const [components, setComponents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchComponents = async () => {
      try {
        const data = await componentService.listComponents();
        setComponents(data);
      } catch (error) {
        console.error("Failed to load components", error);
      } finally {
        setLoading(false);
      }
    };
    fetchComponents();
  }, []);

  const onDragStart = (event, component) => {
    // Pass the entire component definition to the drop zone
    console.log("Dragging component - START:", component);
    event.dataTransfer.setData('application/reactflow', JSON.stringify(component));
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <aside className="w-56 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg">
          <MessageSquare size={16} className="text-gray-600" />
          <span className="text-sm font-medium text-gray-700">Chat With AI</span>
        </div>
      </div>
      
      <div className="p-4">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Components
        </h3>
        
        {loading ? (
          <div className="flex justify-center p-4"><Loader2 className="animate-spin text-gray-400"/></div>
        ) : (
          <div className="space-y-2">
            {components.map((comp) => {
              const Icon = ICON_MAP[comp.type] || MessageSquare;
              return (
                <div
                  key={comp.id}
                  className="flex items-center gap-2 px-3 py-2 border border-gray-200 rounded-md bg-white hover:bg-gray-50 cursor-grab transition-colors"
                  onDragStart={(event) => onDragStart(event, comp)}
                  draggable
                >
                  <Icon size={16} className="text-gray-600" />
                  <span className="text-sm text-gray-700">{comp.name}</span>
                  <span className="ml-auto text-gray-400">⋮⋮</span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </aside>
  );
}