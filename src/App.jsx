import { Routes, Route } from "react-router-dom";
import Proposal from "./pages/Proposal";
import Valentine from "./pages/Valentine";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Proposal />} />
      <Route path="/valentine" element={<Valentine />} />
    </Routes>
  );
}
