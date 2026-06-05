import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Proposal() {
  const navigate = useNavigate();
  const [noCount, setNoCount] = useState(0);
  const [pos, setPos] = useState({ top: "60%", left: "55%" });

  const messages = [
    "Are you sure? 👀",
    "Coffee isn't that scary ☕",
    "I promise I don't bite 😄",
    "You're running out of excuses 😂",
    "Okay, now you're just being difficult 😜",
  ];

  const moveNo = () => {
    setNoCount((prev) => {
      if (prev >= 4) return prev + 1;

      const top = Math.random() * 70 + 10 + "%";
      const left = Math.random() * 70 + 10 + "%";

      setPos({ top, left });

      return prev + 1;
    });
  };

  const handleYes = () => {
    window.open(
      "https://wa.me/918879896069?text=Hi Atharva! Yes, I'd love to go for coffee with you ☕❤️",
      "_blank"
    );

    navigate("/valentine");
  };

  return (
    <div
      className="h-screen w-screen relative overflow-hidden
      bg-gradient-to-br from-pink-200 via-pink-100 to-rose-200
      flex items-center justify-center"
    >
      {/* Floating Background */}
      <div className="absolute inset-0 opacity-25 pointer-events-none">
        <div className="absolute top-20 left-20 text-6xl animate-bounce">
          ☕
        </div>
        <div className="absolute top-32 right-24 text-5xl animate-pulse">
          🍪
        </div>
        <div className="absolute bottom-24 left-24 text-6xl animate-bounce">
          ✨
        </div>
        <div className="absolute bottom-20 right-20 text-5xl animate-pulse">
          🌷
        </div>
      </div>

      {/* Main Card */}
      <div
        className="relative bg-white/80 backdrop-blur-lg
        px-10 py-12 rounded-[2rem]
        shadow-2xl border border-white/50
        text-center max-w-xl w-[90%]
        animate-fadeIn"
      >
        <div className="text-5xl mb-4">☕✨</div>

        <h1 className="text-4xl md:text-5xl font-bold text-pink-600 mb-5">
          Hey Shruti
        </h1>

        <p className="text-xl text-gray-700 leading-relaxed mb-6">
          I was thinking...
          <br />
          Instead of endlessly texting and pretending we're productive,
          how about we grab a coffee and have an actual conversation? ☕
        </p>

        <div className="bg-pink-50 rounded-2xl p-5 mb-8 text-left shadow-sm">
          <p className="font-semibold text-pink-600 mb-3 text-center">
            Why this is a good idea:
          </p>

          <ul className="text-gray-700 space-y-2">
            <li>☕ Good coffee</li>
            <li>😂 Potentially good jokes</li>
            <li>📵 No awkward Zoom calls</li>
            <li>✨ A memorable afternoon</li>
            <li>🤝 Zero pressure, just good company</li>
          </ul>
        </div>

        <div className="flex justify-center">
          <button
            onClick={handleYes}
            className="px-10 py-3
            bg-pink-500 text-white text-lg font-semibold
            rounded-full shadow-lg
            hover:bg-pink-600 hover:scale-105
            transition-all duration-300"
          >
            Count Me In ☕
          </button>
        </div>

        <p className="mt-6 text-gray-500 italic">
          Fair warning: I may ask about your favourite coffee order.
        </p>
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
          No 🙈
        </button>
      )}

      {/* Funny Messages */}
      {noCount > 0 && noCount <= 5 && (
        <p className="absolute bottom-16 text-lg font-medium text-pink-600 animate-bounce">
          {messages[Math.min(noCount - 1, messages.length - 1)]}
        </p>
      )}
    </div>
  );
}