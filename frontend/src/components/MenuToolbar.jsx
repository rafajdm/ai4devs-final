import React from "react";

const MenuToolbar = () => {
  return (
    <header className="fixed top-0 left-0 right-0 w-full bg-gray-800 text-white py-4 px-6 flex items-center justify-start border-b border-gray-600">
      {/* MVP Name in a clean, modern font */}
      <div className="font-sans text-xl font-bold">Promo-finder MVP</div>
    </header>
  );
};

export default MenuToolbar;
