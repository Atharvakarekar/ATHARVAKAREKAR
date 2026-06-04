import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Proposal() {
  const navigate = useNavigate();
  const [noCount, setNoCount] = useState(0);
  const [pos, setPos] = useState({ top: "60%", left: "55%" });

  const moveNo = () => {
    setNoCount((prev) => {
      if (prev >= 4) return prev + 1;

      const top = Math.random() * 70 + 10 + "%";
      const left = Math.random() * 70 + 10 + "%";
      setPos({ top, left });

      return prev + 1;
    });
  };

  return (
    <div className="h-screen w-screen relative overflow-hidden
      bg-gradient-to-br from-pink-200 via-pink-100 to-rose-200
      flex items-center justify-center">

      {/* Background hearts */}
      <div className="absolute inset-0 opacity-25 pointer-events-none">
        <div className="absolute top-20 left-24 text-6xl">🧋</div>
        <div className="absolute top-40 right-32 text-5xl">🥐</div>
        <div className="absolute bottom-28 left-40 text-6xl">🍪</div>
        <div className="absolute bottom-16 right-24 text-5xl">🍫</div>
      </div>

      {/* Main Card */}
      <div className="relative bg-white/70 backdrop-blur-md
        px-12 py-14 rounded-3xl shadow-2xl
        text-center max-w-lg w-[90%]
        animate-fadeIn">

        <h1 className="text-4xl md:text-5xl font-bold text-pink-600 mb-4">
          Hey Krushnali
        </h1>

        <p className="text-xl md:text-2xl text-gray-700 mb-8">
          Life's too short for bad coffee and missed chances so, will you go on a coffee with me? ☕

        </p>

        <div className="flex gap-6 justify-center relative">
          <button
            onClick={() => navigate("/valentine")}
            className="px-10 py-3
              bg-pink-500 text-white text-lg
              rounded-full shadow-md
              hover:bg-pink-600 hover:scale-105
              transition-all duration-300"
          >
            Yes 💖
          </button>
        </div>
      </div>

      {/* No Button */}
      {noCount < 5 && (
        <button
          onMouseEnter={moveNo}
          onTouchStart={moveNo}
          style={{
            position: "absolute",
            top: pos.top,
            left: pos.left,
          }}
          className="px-6 py-2
            bg-gray-200 text-gray-700
            rounded-full shadow
            hover:bg-gray-300
            transition-all duration-200"
        >
          No 😬
        </button>
      )}

      {/* Tease text */}
      {noCount >= 5 && (
        <p className="absolute bottom-16 text-lg font-medium text-pink-600 animate-bounce">
          Ab toh maan jao 💕
        </p>
      )}
    </div>
  );
}
