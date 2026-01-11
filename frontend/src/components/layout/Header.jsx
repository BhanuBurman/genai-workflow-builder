import { Sparkles, Save } from "lucide-react";
export default function Header({ onSave }) {
  return (
    <header className="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-6 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-lg flex items-center justify-center">
          <Sparkles size={18} className="text-white" />
        </div>
        <span className="font-semibold text-gray-900 text-lg">GenAI Stack</span>
      </div>

      <button
        onClick={onSave}
        className="px-4 py-1.5 bg-white border border-gray-300 text-gray-700 rounded-md text-sm font-medium hover:bg-gray-50 transition-colors flex items-center gap-2"
      >
        <Save size={14} />
        Save
      </button>
    </header>
  );
}
