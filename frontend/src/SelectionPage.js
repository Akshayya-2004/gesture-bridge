import { useNavigate } from "react-router-dom";

const SelectionPage = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <h1 className="text-2xl font-bold mb-6">Choose an Option</h1>
      <button className="mb-4 p-3 bg-blue-600 rounded-lg" onClick={() => navigate("/chat")}>
        Chat
      </button>
      <button className="p-3 bg-green-600 rounded-lg" onClick={() => navigate("/detect")}>
        Detect
      </button>
    </div>
  );
};

export default SelectionPage;
