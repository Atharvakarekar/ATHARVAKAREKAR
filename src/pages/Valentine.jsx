import bear from "../assets/bear.png";
export default function Valentine() {

return ( <div

   className="h-screen w-screen relative overflow-hidden

   bg-gradient-to-br from-amber-100 via-rose-100 to-pink-200

   flex items-center justify-center"

 >

{/* Floating background elements */} <div className="absolute inset-0 opacity-25 pointer-events-none"> <div className="absolute top-20 left-20 text-6xl animate-bounce">

☕ </div> <div className="absolute top-32 right-24 text-5xl animate-pulse">

🌷 </div> <div className="absolute bottom-32 left-32 text-6xl animate-bounce">

🤎 </div> <div className="absolute bottom-20 right-20 text-5xl animate-pulse">

✨ </div> <div className="absolute top-1/2 left-10 text-4xl animate-pulse">

💕 </div> <div className="absolute top-1/3 right-10 text-4xl animate-bounce">

🌹 </div> </div>



```

  {/* Main Card */}

  <div

    className="relative bg-white/80 backdrop-blur-lg

    px-12 py-14 rounded-[2rem]

    shadow-2xl border border-white/50

    text-center max-w-lg w-[90%]

    animate-fadeIn"

  >

    <img

      src={bear}
      alt="cute bear"

      className="mx-auto mb-6 w-40 drop-shadow-lg animate-bounce"

    />



    <div className="text-4xl mb-4">☕🌹✨</div>



    <h1 className="text-4xl md:text-5xl font-bold text-pink-600 mb-5">

      You said yes! 💖

    </h1>



    <p className="text-xl md:text-2xl text-gray-700 font-medium leading-relaxed">

      I had a feeling you might...

    </p>



    <p className="mt-6 text-lg text-gray-600 leading-relaxed">

      Now I officially owe you a great coffee,

      <br />

      some good conversations,

      <br />

      and a chance to make you smile a little more than usual. ☕✨

    </p>



    <div className="mt-8 text-3xl">

      🌷 🤎 ☕ 🤍 🌷

    </div>



    <p className="mt-8 text-pink-500 font-semibold text-lg">

      Looking forward to our coffee date already. ☺️

    </p>



    <p className="mt-3 text-gray-500 italic">

      P.S. You just made someone's day a lot better. ❤️

    </p>

  </div>

</div>



);

}
