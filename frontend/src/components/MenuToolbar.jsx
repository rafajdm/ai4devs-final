import React from 'react';

const MenuToolbar = () => {
    return (
        <header className="w-full bg-gray-800 text-white py-4 px-6 flex items-center justify-start border-b border-gray-600 border-4 border-red-500">
            {/* MVP Name in a clean, modern font */}
            <div className="font-sans text-xl font-bold">
                Promo-finder MVP
            </div>
        </header>
    );
};

export default MenuToolbar;